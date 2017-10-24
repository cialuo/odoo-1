# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,exceptions
import datetime

class WarrantyPlan(models.Model): # 车辆保养计划
    _inherit = 'mail.thread'
    _name = 'warranty_plan'
    _order = 'id desc'
    name = fields.Char(string='Warranty Plan', required=True, index=True)

    plan_month = fields.Date(default=datetime.datetime.utcnow())

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

    company_id = fields.Many2one('hr.department', string='Company', related='create_name.department_id')

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
            ('approval_warranty_category', '=', mantaintype),
            ('state', '=', 'done')
        ]
        result = self.env['warranty_plan_order'].search(constrains, order='planned_date desc', limit=1)
        if len(result) > 0:
            return result[0].planned_date
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
            constrains.append(('relateddate', '>', startDate))
        if endDate != None:
            constrains.append(('relateddate', '<', endDate))
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
                lastmantaindate = self.planItemLastCheck(item.id, mitem.id)
                # 计算从上一次维保后又行驶了多少公里
                mileageOffset = self.sumVehicleDriveMileage(item.id,
                                                            None,
                                                            datetime.datetime.today())
                if lastmantaindate == None:
                    # 之前从未做过维保则添加到计划则不加入
                    continue
                    #
                    # itemsToAdd.append(self.constructPlanItemData(item.id,
                    #                                              mitem.warranty_category_id.id,
                    #                                              mileageOffset,
                    #                                              datetime.datetime.today(),
                    #                                              item.daily_mileage,
                    #                                              lastmantaindate))
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
                                                                     lastmantaindate))
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
