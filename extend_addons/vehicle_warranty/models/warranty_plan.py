# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,exceptions
import datetime

class WarrantyPlan(models.Model): # 车辆保养计划
    _inherit = 'mail.thread'
    _name = 'warranty_plan'
    _order = 'id desc'
    name = fields.Char(string='Warranty Plan', required=True, index=True)

    plan_month = fields.Date(default=fields.Date.today)

    @api.depends('plan_month')
    def _compute_month(self):
        for plan in self:
            tmp_plan_month = datetime.datetime.strftime(datetime.datetime.strptime(plan.plan_month, '%Y-%m-%d'), '%Y-%m')
            plan.month=tmp_plan_month

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    month = fields.Char(compute='_compute_month') # 月度

    create_name = fields.Many2one('hr.employee', string="Create Name", default=_default_employee, readonly=True) # required=True,

    # 报单公司
    companyid = fields.Many2one('res.company', string="report company", default=lambda self: self.env.user.company_id,
                                readonly=True)

    made_company_id = fields.Many2one('hr.department', string='Made Company', related='create_name.department_id')


    auditor_id = fields.Many2one('hr.employee', string="Auditor Man",copy=False)
    auditor_time = fields.Datetime(string="Auditor Time",copy=False)

    approval_id = fields.Many2one('hr.employee', string="Approval Man",copy=False)
    approval_time = fields.Datetime(string="Approval Time",copy=False)

    remark = fields.Char()

    state = fields.Selection([
        ('draft', 'draft'), # 草稿
        ('commit', 'commit'), # 已提交
        ('audit', 'audit'), # 已审核
        ('execute', 'execute'), # 执行中
        ('done', 'done'), # 完成
    ], readonly=True, default='draft', string="MyState")

    def planitemExist(self, vehicleid, mantaintype):
        # 检查某辆车的一条维保项目是否已经做过计划
        constrains = [
            ('vehicle_id', '=', vehicleid),
            ('approval_warranty_category', '=', mantaintype),
            ('state', '!=', 'done')
        ]
        result = self.env['warranty_plan_order'].search(constrains, limit=1)
        if len(result)>0:
            return True
        else:
            return False

    def planItemLastCheck(self, vehicleid, mantaintype):
        # 获取车辆维保项的最近一次维保记录
        constrains = [
            ('vehicle_id', '=', vehicleid),
            ('warranty_category', '=', mantaintype),
            ('calculate_state', '=', 'calculated')
        ]
        result = self.env['warranty_order'].search(constrains, order='id desc', limit=1)
        if len(result) > 0:
            return result[0]
        else:
            return None

    def constructPlanItemData(self,vehicleid, mantaintype, mileage, plandate, averagemile, lastmantain):
        # 构造计划详情数据
        data = {
            'vehicle_id':vehicleid,                 # 车辆id
            'warranty_category':mantaintype,        # 保养类型
            'operating_mileage':mileage,            # 增加里程
            'planned_date':plandate,                # 计划日期
            'average_daily_kilometer':averagemile,  # 日平均公里数
        }
        if lastmantain != None:
            data['warranty_location'] = lastmantain.warranty_location
        return data

    def sumVehicleDriveMileage(self, vehicleid, startDate, endDate):
        # 计算在某个时间区间内 车辆的行驶里程
        constrains = [
            ('vehicle_id', '>', vehicleid)
        ]
        if startDate != None:
            constrains.append(('relateddate', '>=', startDate))
        if endDate != None:
            constrains.append(('relateddate', '<=', endDate))
        result = self.env['vehicleusage.driverecords'].search(constrains)
        total = 0
        for item in result:
            total += item.planmileage
        return total

    @api.multi
    def generateDetail(self):
        # 只取运营期车辆
        vehicles = self.env['fleet.vehicle'].search([('vehicle_life_state','=', 'operation_period')])
        # 可提前天数
        predays = 7
        # 缓存车型数据
        vmodel_cache = {}
        itemsToAdd = []
        for item in vehicles:
            mantainitems = vmodel_cache.get(item.model_id.id, None)
            if mantainitems == None:
                # 缓存车型的保养项目列表
                mantainitems = [i for i in item.model_id.warranty_interval_ids]
                vmodel_cache[item.model_id.id] = mantainitems
            for mitem in mantainitems:
                if self.planitemExist(item.id, mitem.id):
                    # 该任务已做计划 跳过
                    continue
                lastmantain = self.planItemLastCheck(item.id, mitem.warranty_category_id.id)
                lastmdate = None
                if lastmantain != None:
                    lastmdate = lastmantain.calculate_time
                # 计算从上一次维保后又行驶了多少公里
                mileageOffset = self.sumVehicleDriveMileage(item.id,
                                                            lastmdate,
                                                            datetime.datetime.today())
                if lastmantain == None:
                    # 之前从未做过维保则添加到计划则不加入
                    continue
                else:
                    bigestmileage = mileageOffset + predays*item.daily_mileage
                    if (bigestmileage) > (mitem.interval_mileage - mitem.warranty_category_id.active_mileage):
                        # 如果加上提前天数满足维保里程阈值则添加到维保记录
                        dayoffset = int((bigestmileage-mitem.interval_mileage)/item.daily_mileage)
                        plandate = datetime.datetime.today()+datetime.timedelta(days=abs(predays-dayoffset))
                        itemsToAdd.append(self.constructPlanItemData(item.id,
                                                                     mitem.warranty_category_id.id,
                                                                     mileageOffset,
                                                                     plandate,
                                                                     item.daily_mileage,
                                                                     lastmdate))
                    else:
                        continue
        sqldata = [(0, 0, item) for item in itemsToAdd]
        self.write({'plan_order_ids':sqldata})
        return self

    @api.multi
    def action_draft(self):
        self.state = 'draft'
        for plan_order in self.plan_order_ids:
            plan_order.state = 'draft'

    @api.multi
    def action_commit(self):

        """新增数据验证：
            确认时判断是否存在计划详情!
        """
        if len(self.plan_order_ids) == 0:
            raise exceptions.UserError(_('Program details can not be empty.'))

        self.state = 'commit'
        for plan_order in self.plan_order_ids:
            if plan_order.state == 'draft':
                plan_order.state = 'commit'


    @api.multi
    def action_audit(self):
        self.state = 'audit'
        self.auditor_id = self._default_employee()
        self.auditor_time = datetime.datetime.utcnow()

    @api.multi
    def action_execute(self):
        self.state = 'execute'
        self.approval_id = self._default_employee()
        self.approval_time = datetime.datetime.utcnow()
        for plan_order in self.plan_order_ids:
            if plan_order.state == 'commit':
                plan_order.state = 'wait'
            plan_order.vehicle_id.state = 'warrantly'


    @api.multi
    def action_done(self):
        self.state = 'done'

    plan_order_ids = fields.One2many('warranty_plan_order', 'parent_id', 'sheetIds',required=True) # 计划单ids

    @api.depends('plan_order_ids')
    def _compute_task_count(self):
        plan_sheet_count=0 # 任务数
        maintain_sheet_count=0 # 已执行
        for plan in self:
            for plan_sheet in plan.plan_order_ids:
                plan_sheet_count += 1
                if plan_sheet.maintain_sheet_id.id:
                    maintain_sheet_count += 1
            plan.task_count=plan_sheet_count
            plan.executed_count=maintain_sheet_count

    task_count = fields.Integer(default=0, compute='_compute_task_count') # 任务数

    executed_count = fields.Integer(default=0, compute='_compute_task_count') # 已执行

    @api.model
    def create(self, vals):
        result = super(WarrantyPlan, self.with_context(mail_create_nolog=True)).create(vals)
        result.message_post(body=_('%s has been added to the plan!') % (result.name,))
        return result

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, name=_('%s (copy)') % self.name)
        res = super(WarrantyPlan, self).copy(default)
        for line in self.plan_order_ids:
            line.copy({'parent_id': res.id, 'maintain_sheet_id': '', 'state': 'draft'}) #
        return res



class WarrantyPlanOrder(models.Model): # 计划详情单
    _name = 'warranty_plan_order'
    _order = 'id desc'
    name = fields.Char(string="Warranty Plan Order", required=True, index=True, default='/')

    # 车辆保养计划ID
    parent_id = fields.Many2one('warranty_plan', 'Warranty Plan', required=True, ondelete='cascade')

    sequence = fields.Integer('Sequence', default=1)

    # 车号
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", required=True,
                                 domain=[('entry_state', '=', 'audited'),
                                         ('vehicle_life_state', '=', 'operation_period'),
                                         ('state', '!=', 'stop')])
    # 车型
    vehicle_type = fields.Many2one("fleet.vehicle.model",related='vehicle_id.model_id', store=True, readonly=True)

    # 车牌
    license_plate = fields.Char("License Plate", related='vehicle_id.license_plate', store=True, readonly=True)

    #fleet = fields.Char()  # 车队
    fleet = fields.Many2one("res.company", related='vehicle_id.company_id', store=True, readonly=True)

    # 承修公司
    repaircompany = fields.Many2one('res.company', string="repair comany")
    # 保修公司
    report_company = fields.Many2one('res.company', related='parent_id.companyid')

    # 运营里程
    operating_mileage = fields.Float(digits=(6, 1), string="Operating Mileage")

    warranty_category = fields.Many2one('warranty_category', 'Warranty Category',required=True, domain=[('level', '=', '1')]) # 生成保养类别

    @api.one
    @api.depends('warranty_category')
    def _compute_approval_warranty_category(self):
        self.approval_warranty_category = self.warranty_category

    approval_warranty_category = fields.Many2one(
        'warranty_category', 'Approval Warranty Category',
        domain=[('level', '=', '1')], compute='_compute_approval_warranty_category') # 核准保养类别

    planned_date = fields.Date('Planned Date', default=fields.Date.context_today) # 计划日期

    vin = fields.Char(related='vehicle_id.vin_sn', store=True, readonly=True) # 车架号

    average_daily_kilometer = fields.Float(digits=(6, 1), string="Average Daily Kilometer") # 平均日公里

    line = fields.Many2one("route_manage.route_manage", related='vehicle_id.route_id', store=True, readonly=True) # 线路

    #保养地点
    warranty_location = fields.Many2one('vehicle.plant')

    maintain_sheet_id = fields.Many2one('warranty_order', string="Warranty Maintain Sheet")  # 保养单号 , required=True,

    report_repair_user = fields.Many2one('hr.employee', string="Report Name")  # 报修人 , required=True

    state = fields.Selection([ # 状态
        ('draft', "draft"), # 草稿
        ('commit', 'commit'), # 已提交
        ('wait', "wait"), # 等待执行
        ('executing', "executing"), # 正在执行
        ('done', "done"), # 执行完毕
    ], default='draft', string="MyState")

    @api.onchange('warranty_category','vehicle_id')
    def _onchange_warranty_category(self):
        """
            保养类型变更时：
                查询当前车辆的最后一次保养的维修厂
        :return:
        """
        if self.warranty_category and self.vehicle_id:
            domain = [('vehicle_id','=',self.vehicle_id.id),
                      ('warranty_category','=',self.warranty_category.id),('state','=','done')]
            warranty_order = self.env['warranty_order'].search(domain,limit=1,order="warranty_end_time desc")

            if warranty_order:
                self.warranty_location = warranty_order.warranty_location



    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def unlink(self):
        for order in self:
            if order.state not in ['wait', 'draft', 'commit']:
                raise exceptions.UserError(_('warranty in executing or have done, can not be deleted!'))

        return super(WarrantyPlanOrder, self).unlink()


class WizardCreateWarrantyOrderByDriver(models.TransientModel): # 计划单生成关联司机的保养单
    _name = 'wizard_create_warranty_order_by_driver'

    def _default_plan_order(self):
        active_ids=self._context.get('active_ids')
        plan_order_ids = self.env['warranty_plan_order'].browse(active_ids)
        return plan_order_ids

    plan_order_ids = fields.Many2many('warranty_plan_order', string='Warranty Plan Order', required=True, default=_default_plan_order)

    @api.multi
    def create_warranty_order_by_driver(self):
        active_ids = self._context.get('active_ids')
        plan_sheets = self.env['warranty_plan_order'].browse(active_ids)
        for plan_sheet in plan_sheets:

            if not plan_sheet.maintain_sheet_id:
                plan = plan_sheet.parent_id
                maintain_sheets = self.env['warranty_order'].search([('plan_id', '=', plan.id)])
                maintain_sheets_count = len(maintain_sheets)
                maintain_sheet_val = {
                    'name': plan.name + '_' + str(maintain_sheets_count + 1),  # +''+str(maintain_sheets_count)
                    'vehicle_id': plan_sheet.vehicle_id.id,
                    'vehicle_type': plan_sheet.vehicle_type.id,
                    'license_plate': plan_sheet.license_plate,
                    'fleet': plan_sheet.fleet.id,
                    'operating_mileage': plan_sheet.operating_mileage,
                    'warranty_category': plan_sheet.approval_warranty_category.id,
                    'planned_date': plan_sheet.planned_date,
                    'vin': plan_sheet.vin,
                    'average_daily_kilometer': plan_sheet.average_daily_kilometer,
                    'line': plan_sheet.line.id,
                    'warranty_location': plan_sheet.warranty_location.id,
                    'plan_id': plan.id,
                    # 'report_repair_user':plan_sheet.report_repair_user.id
                }
                maintain_sheet = self.env['warranty_order'].create(maintain_sheet_val)

                category_id = maintain_sheet.warranty_category.id

                condition = '%/' + str(category_id) + '/%'

                sql_query = """
                                select id,idpath from warranty_category
                                where idpath like %s
                                order by idpath asc
                            """

                self.env.cr.execute(sql_query, (condition,))

                results = self.env.cr.dictfetchall()

                sheet_items = []
                available_products = []
                sheet_instructions = []
                for line in results:
                    category = self.env['warranty_category'].search([('id', '=', line.get('id'))])
                    project_ids = category.project_ids
                    for project in project_ids:
                        order_project = {
                            'warranty_order_id': maintain_sheet.id,
                            'category_id': category.id,
                            'project_id': project.id,
                            'sequence': len(sheet_items) + 1,
                            'work_time': project.manhour,
                            'percentage_work': 100,
                        }

                        sheet_items.append((0, 0, order_project))

                        sheet_instruction = {
                            'warranty_order_id': maintain_sheet.id,
                            'category_id': category.id,
                            'project_id': project.id,
                            'sequence': len(sheet_instructions) + 1
                        }
                        sheet_instructions.append((0, 0, sheet_instruction))

                        warranty_project = self.env['warranty_project'].search([('id', '=', project.id)])
                        boms = warranty_project.avail_ids
                        for bom in boms:
                            available_product = {
                                'sequence': len(available_products) + 1,
                                'warranty_order_id': maintain_sheet.id,
                                'category_id': category.id,
                                'project_id': project.id,
                                'product_id': bom.product_id.id,
                                'change_count': bom.change_count,
                                'max_count': bom.max_count,
                                'require_trans': bom.require_trans,
                                'list_price': bom.list_price
                            }
                            available_products.append((0, 0, available_product))

                maintain_sheet.write({'project_ids': sheet_items, 'available_product_ids': available_products,
                                      'instruction_ids': sheet_instructions})
                plan_sheet.update({'maintain_sheet_id': maintain_sheet.id,
                                   'state': 'executing'})

