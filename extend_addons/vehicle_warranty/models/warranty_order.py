# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
import datetime
from datetime import timedelta
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

class WarrantyOrder(models.Model): # 保养单
    _inherit = 'mail.thread'
    _name = 'warranty_order'
    _order = 'id desc'
    name = fields.Char(string='Warranty Order', required=True, index=True, default='/')

    sequence = fields.Integer('Sequence', default=1)

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", required=True, )  # 车号

    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id', store=True, readonly=True)  # 车型

    license_plate = fields.Char("License Plate", related='vehicle_id.license_plate', store=True, readonly=True)  # 车牌

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    report_repair_user = fields.Many2one('hr.employee', string="Report Name", default=_default_employee, required=True) # 报修人

    operating_mileage = fields.Float(digits=(6, 1), string="Operating Mileage")  # 运营里程

    warranty_category = fields.Many2one('warranty_category', 'Warranty Category', ondelete='cascade', required=True)  # 保养类别

    planned_date = fields.Date('Planned Date', default=fields.Date.context_today)  # 计划日期

    vin = fields.Char("VIN")  # 车架号

    average_daily_kilometer = fields.Float(digits=(6, 1), string="Average Daily Kilometer")  # 平均日公里

    line = fields.Many2one("route_manage.route_manage")  # 线路

    repair_unit = fields.Char()  # 承修单位

    fleet = fields.Many2one("res.company")  # 车队

    maintenance_level = fields.Char()  # 维修等级

    fill_personnel = fields.Char()  # 填单人

    fill_personnel_unit = fields.Char()  # 填单人单位

    remark = fields.Char()  # 备注信息

    warranty_location = fields.Many2one('vehicle.plant')  # 保养地点

    # 修理厂所属部门
    depa_id = fields.Many2one('hr.department', related='warranty_location.department_id',
                              store=True, readonly=True)

    repair_workshop = fields.Many2one('hr.department')  # 承修车间

    state = fields.Selection([ # 状态
        ('dispatch', "dispatch"),
        ('maintain', "maintain"),
        ('inspect', "inspect"),
        ('done', "done"),
    ], default='dispatch', string="MyState")

    plan_order_ids = fields.One2many('warranty_plan_order', 'maintain_sheet_id', 'Plan Order')  # 保养计划单

    #车辆设置
    company_id_stting = fields.Many2one('res.company', 'Company',
                                   default=lambda self: self.env['res.company']._company_default_get('warranty_order'),
                                   index=True, required=True)
    #是否验证数据
    maintenance_settings = fields.Selection(related='company_id_stting.maintenance_settings')


    picking_ids = fields.One2many("stock.picking", 'warranty_order_id', string='Stock Pickings')

    @api.multi
    def create_get_picking(self): # 创建领料单
        picking_type = self.env['stock.picking.type'].search(
            [('name', '=', u'领料'), ('warehouse_id.company_id', '=', self.env.user.company_id.id)])
        self.ensure_one()
        context = dict(self.env.context,
            default_warranty_order_id=self.id,
            default_origin=self.name,
            default_picking_type_id=picking_type.id,
        )
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'res_id': '',
            'context': context
        }

    @api.multi
    def create_back_picking(self): # 创建退料单
        self.ensure_one()
        picking_type = self.env['stock.picking.type'].search(
            [('name', '=', u'退料'), ('warehouse_id.company_id', '=', self.env.user.company_id.id)])
        context = dict(self.env.context,
            default_warranty_order_id=self.id,
            default_origin=self.name,
            default_picking_type_id=picking_type.id,
        )
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'res_id': '',
            'context': context
        }

    @api.multi
    def action_into_maintain(self):  # 保养单_进入保养状态 开工
        self.ensure_one()
        if not self.manhour_manage_ids:
            raise exceptions.UserError(_("Maintain Repair Jobs Required!"))
        self.write({'state': 'maintain'})

        for i in self.manhour_manage_ids:
            i.real_start_time = datetime.datetime.utcnow()
        for project in self.project_ids:
            if project.state == 'dispatch' :
                project.state = 'maintain'
            else:
                raise exceptions.UserError(_("Please batch dispatch first!"))
        avail_products = self.mapped('available_product_ids').filtered(lambda x: x.change_count > 0)
        location_dest_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位
        self._generate_picking(avail_products, location_dest_id)

    def _generate_picking(self, products, location):
        picking_type = self.env['stock.picking.type'].search(
            [('name', '=', u'发料'), ('warehouse_id.company_id', '=', self.env.user.company_id.id)])

        location_id = picking_type.default_location_src_id.id or picking_type.warehouse_id.lot_stock_id.id

        for products in [products]:
            if not products:
                continue
            move_lines = []
            picking = []
            for i in products:
                vals = {
                    'name': 'stock_move_repair',
                    'product_id': i.product_id.id,
                    'product_uom': i.product_id.uom_id.id,
                    'product_uom_qty': i.change_count,
                    'picking_type_id': picking_type.id,
                }
                move_lines.append((0, 0, vals))
            if move_lines:
                picking = self.env['stock.picking'].create({
                    'origin': self.name,
                    'location_id': location_id,
                    'location_dest_id': location,
                    'picking_type_id': picking_type.id,
                    'warranty_order_id': self.id,
                    'move_lines': move_lines
                })
            if picking:
                picking.action_confirm()



    @api.multi
    def action_into_inspect(self):  # 保养单_全部报检
        self.ensure_one()
        if not self.manhour_manage_ids:
            raise exceptions.UserError(_("Manhour Manage Ids Required!"))
        self.write({'state': 'inspect'})

        for i in self.manhour_manage_ids:
            i.real_end_time = datetime.datetime.utcnow()
        for project in self.project_ids:
            project.state = 'check'


    plan_id = fields.Many2one('warranty_plan', 'Plan Id', required=True, ondelete='cascade')  # 车辆保养计划ID

    project_ids = fields.One2many('warranty_order_project', 'warranty_order_id', 'Warranty Order') # 保养项目

    manhour_manage_ids = fields.One2many('warranty_order_manhour', 'warranty_order_id', 'Warranty Order') # 工时管理

    available_product_ids = fields.One2many('warranty_order_product', 'warranty_order_id', 'Warranty Order') # 可领物料

    instruction_ids = fields.One2many('warranty_order_instruction', 'warranty_order_id', 'Warranty Order') # 作业指导

    return_record_ids = fields.One2many('warranty_order_reject', 'warranty_order_id', 'Warranty Order') # 退检记录

    # 2017年7月25日 新增字段：保养总时长,保养开始时间，保研结束时间
    warranty_total_time = fields.Float(string='Warranty total time', readonly=True,
                                       digits=dp.get_precision('Operate pram'), compute='_compute_warranty_total_time')
    warranty_start_time = fields.Datetime(related='plan_id.approval_time',string='Warranty start time')
    warranty_end_time = fields.Datetime(compute='compute_warranty_end_time')

    @api.depends('project_ids')
    def compute_warranty_end_time(self):
        """
            获取检验单内的的最后一个检验通过时间
        :return:
        """
        for order in self:

            if order.project_ids.mapped('state').count('complete') == len(order.project_ids):
                #所有检验单完成情况下，取最后一个时间
                order.warranty_end_time = max(order.project_ids.mapped('end_inspect_time'))



    @api.depends('warranty_start_time', 'warranty_end_time')
    def _compute_warranty_total_time(self):
        """
            计算保养总时长
        :return:
        """
        for order in self:
            if order.warranty_end_time and order.warranty_start_time:
                warranty_end_time = datetime.datetime.strptime(order.warranty_end_time, "%Y-%m-%d %H:%M:%S")
                warranty_start_time = datetime.datetime.strptime(order.warranty_start_time, "%Y-%m-%d %H:%M:%S")
                warrant_time = warranty_end_time - warranty_start_time
                days, seconds = warrant_time.days, warrant_time.seconds
                if days >= 0 and seconds >= 0:
                    hours = days * 24 + seconds // 3600
                    order.warranty_total_time = hours


    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('warranty_plan.order') or '/'

        result = super(WarrantyOrder, self.with_context(mail_create_nolog=True)).create(vals)
        result.message_post(body=_('%s has been added to the Warranty Order!') % (result.name,))
        return result

    def if_complete_dispatch(self):
        total_manhour = sum([manhour.percentage_work for manhour in self.manhour_manage_ids])
        sum_manhour = len(self.project_ids)*100
        if total_manhour == sum_manhour:
            return True
        elif total_manhour > sum_manhour:
            raise exceptions.ValidationError(_('this "percentage_work" may not be Incorrect'))


    @api.multi
    def action_batch_dispatch(self): # 保养单_批量派工

        return {
            'name': _('Batch Dispatch'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard_batch_dispatch', # 'res_model': 'hr.expense.sheet',
            'context': {
            },
            'view_id': self.env.ref('vehicle_warranty.wizard_batch_dispatch_form').id,
            'target': 'new'
        }

    @api.multi
    def action_inspect_order(self): # 查看检验单
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('vehicle_warranty', xml_id)
            res.update(
                domain=[('warranty_order_id', '=', self.id)]
            )
            return res
        return False



    @api.multi
    def unlink(self):
        for order in self:
            if not order.state=='draft':
                raise exceptions.UserError(_('warranty order not in draft state can not delete'))

            for plan_order_id in order.plan_order_ids:
                plan_order_id.maintain_sheet_id=''
                plan_order_id.state='wait'

        return super(WarrantyOrder, self).unlink()




class WarrantyOrderProject(models.Model): # 保养单_保养项目
    _name = 'warranty_order_project'
    _order = "warranty_order_id,sequence"

    name = fields.Char(related='project_id.name') # related='project_id.name', store=True

    sequence = fields.Integer(default=1)

    warranty_order_id = fields.Many2one('warranty_order', index=True) # 所属保养单

    category_id = fields.Many2one('warranty_category') # 保养类别

    project_id = fields.Many2one('warranty_project', 'Warranty Project', required=True) # 保养项目

    warranty_mode = fields.Many2one('warranty_mode', 'Warranty Mode', related='project_id.mode')  # 保修方式

    vehicle_id = fields.Many2one('fleet.vehicle', related='warranty_order_id.vehicle_id', store=True, readonly=True)  # 车号

    vehicle_type = fields.Many2one("fleet.vehicle.model", related='warranty_order_id.vehicle_id.model_id')  # 车型

    license_plate = fields.Char("License Plate", related='warranty_order_id.vehicle_id.license_plate')  # 车牌

    maintenance_personnel = fields.Char(compute='_get_maintenance_personnel_names')  # 保养人员

    # @api.depends("manhour_manage_ids")
    def _get_maintenance_personnel_names(self):  #获取维修人名字
        for i in self:
            names = set()
            for j in i.manhour_manage_ids:
                names.add(j.user_id.name)
            i.maintenance_personnel = ",".join(list(names))

    state = fields.Selection([ # 状态
        ('nodispatch', ""), # 待派工
        ('dispatch', "dispatch"), # 派工
        ('maintain', "maintain"), # 保养
        ('check', "check"), # 检验
        ('complete', "complete"), # 完成
    ], default='nodispatch', string="MyState")

    inspection_operation = fields.Selection([ # 报检操作
        ('noinspection', ""),
        ('inspection', "inspection"),
    ], default='noinspection')

    return_record_ids = fields.One2many("warranty_order_reject", 'order_project', string='Return Record Ids')

    rework_count = fields.Integer("Rework Count", help="Rework Count", compute="_get_rework_count")  # 重检次数

    def _get_rework_count(self):  # 获取退检次数
        for i in self:
            i.rework_count = len(i.return_record_ids)

    work_time = manhour = fields.Float(digits=(6, 1)) # 工时定额 # fields.Integer('WorkTime') # work_time = fields.Integer(related='fault_method_id.work_time', store=True, readonly=True, copy=False)

    #修理厂所属部门
    depa_id = fields.Many2one('hr.department', related='warranty_order_id.warranty_location.department_id',
                                    store=True, readonly=True)
    user_id = fields.Many2one('hr.employee', string="Repair Name", ondelete='set null')
    plan_start_time = fields.Datetime("Plan Start Time", default=fields.Datetime.now)
    plan_end_time = fields.Datetime("Plan End Time", compute='_get_end_datetime') # ,compute='_get_end_datetime'

    @api.depends('plan_start_time')
    def _get_end_datetime(self):
        for r in self:
            if not (r.plan_start_time and r.work_time):
                continue
            start = fields.Datetime.from_string(r.plan_start_time)
            r.plan_end_time = start + timedelta(seconds=r.work_time*60)

    percentage_work = fields.Float(compute='on_change_manhour_manage_ids', digits=(6, 1))

    @api.onchange('percentage_work')
    def _verify_valid_percentage_work(self):
        if self.percentage_work < 0 or self.percentage_work > 100:
            return {
                'warning': {
                    'title': _("Incorrect 'percentage_work' value"),
                    'message': _("The percentage_work may not be Incorrect"),
                },
            }

    @api.depends('manhour_manage_ids')
    def on_change_manhour_manage_ids(self):

        self.percentage_work = 100 - sum(self.manhour_manage_ids.mapped('percentage_work'))


    manhour_manage_ids = fields.One2many("warranty_order_manhour", 'project_id', string='Manhour Manage')

    @api.multi
    def dispatch(self): # 派工
        self.ensure_one()
        if not self.user_id:
            raise exceptions.UserError(_("user_id Required!"))

        manhour_percentage_work = 0
        for manhour_manage in self.manhour_manage_ids:
            manhour_percentage_work += manhour_manage.percentage_work


        percentage_work=self.percentage_work+manhour_percentage_work

        if percentage_work < 0 or percentage_work > 100:
            raise exceptions.ValidationError(_('"percentage_work" may not be Incorrect'))

        vals = {
            "plan_start_time": self.plan_start_time,
            "plan_end_time": self.plan_end_time,
            "work_time": self.work_time,
            "percentage_work": self.percentage_work,
            # 'self_work': self_work,
            "user_id":self.user_id.id,
            "sequence":len(self.manhour_manage_ids)+1,
            "warranty_order_id":self.warranty_order_id.id
        }

        self.percentage_work=100-percentage_work
        self.state = 'dispatch'

        self.write({'manhour_manage_ids': [(0, 0, vals)]})


    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.warranty_order_id.name:
                name = record.warranty_order_id.name + '/' + name
            res.append((record.id, name))
        return res


class WarrantyOrderManhour(models.Model): # 保养单_工时管理
    _name = 'warranty_order_manhour'
    _order = "sequence"

    _sql_constraints = [
        ('check_percentage_work_value', 'CHECK (percentage_work > 0 and percentage_work <= 100)', u'额定工时的数值在100以内！')
    ]

    name = fields.Char("Manhour")

    sequence = fields.Integer()

    project_id = fields.Many2one("warranty_order_project", ondelete='cascade',string="WarrantyProject") # 所属保养项目

    project_category_id = fields.Many2one('warranty_category', related='project_id.category_id') # 所属保养项目的保养类别

    project_project_id = fields.Many2one('warranty_project', 'Warranty Project', related='project_id.project_id') # 所属保养项目的保养项目

    user_id = fields.Many2one('hr.employee', string="Warranty Man", required=True) # 保养人员

    plan_start_time = fields.Datetime("Plan Start Time") # 计划开工时间

    plan_end_time = fields.Datetime("Plan End Time") # 计划完工时间

    real_start_time = fields.Datetime("Real Start Time") # 实际开工时间

    real_end_time = fields.Datetime("Real End Time") # 实际完工时间

    work_time = fields.Float(digits=(6, 1)) # 额定工时

    percentage_work = fields.Float(digits=(6, 1)) # 工时比例

    self_work = fields.Float(digits=(6, 1), compute='_get_self_work') # 本人工时

    @api.depends('work_time', 'percentage_work')
    def _get_self_work(self):
        for r in self:
            if not (r.percentage_work and r.work_time):
                continue
            r.self_work = r.percentage_work * r.work_time / 100

    real_work = fields.Float(digits=(6, 1), compute='_get_real_work') # 实际工时
    real_work_fee = fields.Float('Real Work Fee', digits=(10, 2))

    @api.depends('real_start_time', 'real_end_time')
    def _get_real_work(self):
        for r in self:
            if not (r.real_start_time and r.real_end_time):
                continue
            start_time = fields.Datetime.from_string(r.real_start_time)
            end_time = fields.Datetime.from_string(r.real_end_time)
            r.real_work = (end_time - start_time).seconds / 3600.0

    warranty_order_id = fields.Many2one('warranty_order', index=True)

    @api.constrains('percentage_work')
    def check_percentage_work(self):
        """
            检查额定工时的值是否超出界限
        :return:
        """
        project_ids = self.mapped('project_id')
        for project in project_ids:
            manhours = self.env['warranty_order_manhour'].search([('project_id', '=', project.id)])
            total = sum(manhours.mapped('percentage_work'))
            if total < 0 or total > 100:
                raise exceptions.ValidationError(_("Please check the allocation of deadline!"))




class WarrantyOrderProduct(models.Model): # 保养单_可领物料
    _name = 'warranty_order_product'

    sequence = fields.Integer("Sequence")

    warranty_order_id = fields.Many2one('warranty_order', ondelete='set null', string="Warranty Order", index=True) # 所属保养单

    category_id = fields.Many2one('warranty_category') # 保养类别

    project_id = fields.Many2one('warranty_project', 'Warranty Project')  # 保养项目

    product_id = fields.Many2one('product.product', 'Product', required=True) # 物资

    product_code = fields.Char('Product Code', related='product_id.default_code') # 物资编码 , store=True, readonly=True

    categ_id = fields.Many2one('product.category', related='product_id.categ_id', string='Warranty Category')

    uom_id = fields.Many2one('product.uom', 'Unit of Measure', related='product_id.uom_id')

    onhand_qty = fields.Float('Quantity On Hand', related='product_id.qty_available')

    virtual_available = fields.Float('Forecast Quantity', related='product_id.virtual_available')

    require_trans = fields.Boolean("Require Trans", readonly=True)

    vehicle_model = fields.Many2many(related='product_id.vehicle_model', relation='product_vehicle_model_rec', string='Suitable Vehicle', readonly=True)

    product_size = fields.Text("Product Size", related='product_id.description', readonly=True)

    list_price = fields.Float("Stock Price")

    change_count = fields.Integer("Change Count")

    max_count = fields.Integer("Max Count")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_code = self.product_id.code
            self.product_name = self.product_id.name


class WarrantyOrderInstruction(models.Model): # 保养单_作业指导
    _name = 'warranty_order_instruction'
    _order = "sequence"

    sequence = fields.Integer('Sequence', default=1)

    warranty_order_id = fields.Many2one('warranty_order', index=True) # 所属保养单

    category_id = fields.Many2one('warranty_category') # 保养类别

    project_id = fields.Many2one('warranty_project', 'WarrantyProject', required=True) # 保养项目

    warranty_mode = fields.Many2one('warranty_mode', 'Warranty Mode', related='project_id.mode')  # 保修方式

    operational_manual = fields.Text(related='project_id.operational_manual') # 作业手册


class WarrantyInspectOrder(models.Model): # 检验单

    _inherit = 'warranty_order_project'

    inspect_result = fields.Selection([
        ('qualified', 'qualified'), # 合格
        ('defective', 'defective')  # 不合格
    ], string="Inspect Result") # 检验结论

    start_inspect_time = fields.Datetime("Start Inspect Time") # 报检时间

    end_inspect_time = fields.Datetime("End Inspect Time") # 检验通过时间

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    inspect_user_id = fields.Many2one('hr.employee', string="Inspect User", default=_default_employee) # 检验员

    inspection_criteria = fields.Text(related='project_id.inspection_criteria')  # 检验标准

    item_name = fields.Char(related='project_id.name')  # 项目名称


    @api.multi
    def action_check_pass(self):
        for i in self:
            if i.state != 'check':
                raise exceptions.UserError(_("Selected project cannot be complete as they are not in 'check' state"))
            i.state = 'complete'
            i.inspect_result = 'qualified'
            i.end_inspect_time = datetime.datetime.utcnow() # fields.Datetime.now()
            i.vehicle_id.state = 'normal'
            if all(project.state == 'complete' for project in i.warranty_order_id.project_ids):
                i.warranty_order_id.state = 'done'
                i.warranty_order_id.plan_order_ids.state = 'done'
                plan = i.warranty_order_id.plan_order_ids.parent_id
                if all(plan_sheet.state == 'done' for plan_sheet in plan.plan_order_ids):
                    plan.state = 'done'

    @api.multi
    def action_return(self, reason=''): # 退回重修
        inspect_return_time = datetime.datetime.utcnow() # fields.Datetime.now()
        vals = {
            "order_project": self.id,
            "inspect_return_time": inspect_return_time,
            "return_reason": reason,
            "sequence": len(self.return_record_ids) + 1,
            "warranty_order_id": self.warranty_order_id.id
        }
        self.write({
            "state":'maintain',
            "end_inspect_time": inspect_return_time,
            "inspect_result": "defective",
            "return_record_ids": [(0, 0, vals)]
        })


class WarrantyOrderReject(models.Model): # 保养单_退检记录
    _name = 'warranty_order_reject'

    order_project = fields.Many2one('warranty_order_project', string="Sheet WarrantyProject")

    maintainsheet_name = fields.Char(string='Maintainsheet Name', related='order_project.warranty_order_id.name')

    inspect_user_id = fields.Many2one('hr.employee', related='order_project.inspect_user_id', string="Inspect User")

    maintenance_personnel = fields.Char(string='Maintenance Personnel',related='order_project.maintenance_personnel')

    return_reason = fields.Text("Return Reason")

    inspect_return_time = fields.Datetime("Inspect Return Time")

    sequence = fields.Integer("Sequence")

    warranty_order_id = fields.Many2one('warranty_order', ondelete='set null', string="WarrantyOrderId", index=True) # 所属保养单


class WizardBatchDispatch(models.TransientModel): # 保养单_批量派工
    _name = 'wizard_batch_dispatch'

    def _default_sheetId(self):
        active_id = self._context.get('active_id')
        return active_id

    sheetId=fields.Char(default=_default_sheetId)

    def _defaultwarranty_order_id(self):
        """
            获取保养单
        :return:
        """
        active_id = self._context.get('active_id')
        return self.env['warranty_order'].search([('id', '=', active_id)])

    # 2017年7月31日 新增字段:保养单ID
    warranty_order_id = fields.Many2one('warranty_order', default=_defaultwarranty_order_id)

    department_id = fields.Many2one('hr.department',related='warranty_order_id.warranty_location.department_id', store=True, readonly=True)


    project_id = fields.Many2many('warranty_order_project', string='WarrantyProject', required=True) # , default=_default_item


    user_id = fields.Many2many('hr.employee', string="User", required=True)

    @api.multi
    def batch_dispatch(self):

        self.save_batch_dispatch()

        return False

    @api.multi
    def batch_dispatch_continue(self):
        """
            派工并继续
        :return:
        """

        self.save_batch_dispatch()

        return {
            'name': _('Batch Dispatch'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard_batch_dispatch',  # 'res_model': 'hr.expense.sheet',
            'context': {
                'default_sheetId': self.sheetId
            },
            'view_id': self.env.ref('vehicle_warranty.wizard_batch_dispatch_form').id,
            'target': 'new'
        }


    def save_batch_dispatch(self):
        """
            保存派工数据
        :return:
        """
        sheetId = self._context.get('active_id')

        maintain_sheet = self.env['warranty_order'].search([('id', '=', sheetId)])
        manhours = []
        manhour_count = len(maintain_sheet.manhour_manage_ids)

        user_count = len(self.user_id)

        for project in self.project_id:
            sum_manhour_percentage_work = sum(project.manhour_manage_ids.mapped('percentage_work'))

            if sum_manhour_percentage_work == 100:
                continue

            val_manhour_percentage_work = 0

            if sum_manhour_percentage_work > 0 and sum_manhour_percentage_work < 100:
                val_manhour_percentage_work = (100 - sum_manhour_percentage_work) / user_count
            else:
                val_manhour_percentage_work = 100 / user_count

            for user in self.user_id:
                manhour_count += 1

                plan_start_time = datetime.datetime.utcnow()
                plan_end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=project.work_time * 60)

                manhour = {
                    'name': manhour_count,
                    'sequence': manhour_count,
                    'project_id': project.id,
                    'user_id': user.id,
                    'plan_start_time': plan_start_time,
                    'plan_end_time': plan_end_time,
                    'work_time': project.work_time,
                    'percentage_work': val_manhour_percentage_work,
                    'warranty_order_id': sheetId
                }
                manhours.append((0, 0, manhour))
            project.update({
                'state': 'dispatch',
                'percentage_work': 100 - (sum_manhour_percentage_work + val_manhour_percentage_work * user_count)
            })
        maintain_sheet.write({'manhour_manage_ids': manhours})

class WizardInspectOrderReject(models.TransientModel): # 检验单_退回重修
    _name = "wizard_inspect_order_reject"

    return_reason = fields.Text("Return Reason")

    @api.multi
    def reject(self):
        context = dict(self._context or {})
        # print context
        active_id = context.get('active_id', '') or ''
        record = self.env['warranty_order_project'].browse(active_id)
        if record.state != 'check':
            raise UserError(_("Selected project cannot be return as they are not in 'check' state."))
        record.action_return(self.return_reason)
        return {'type': 'ir.actions.act_window_close'}


class WizardInspectOrderBatchReject(models.TransientModel): # 检验单_批量退检
    _name = 'wizard_inspect_order_batch_reject'

    def _default_item(self):
        project_ids=self._context.get('active_ids')
        project_ids = self.env['warranty_order_project'].browse(project_ids)
        return project_ids

    project_ids = fields.Many2many('warranty_order_project', string='WarrantyProject Ids', required=True, default=_default_item)

    return_reason = fields.Text("Return Reason")

    @api.multi
    def reject(self):
        project_ids = self._context.get('active_ids')
        project_ids = self.env['warranty_order_project'].browse(project_ids)

        for project in project_ids:
            if project.state != 'check':
                raise UserError(_("Selected project cannot be return as they are not in 'check' state."))
            project.action_return(self.return_reason)


class WizardProjectBatchToCheck(models.TransientModel): # 保养项目_批量_报检
    _name = "wizard_project_batch_to_check"

    @api.multi
    def confirm(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        project_ids = self.env['warranty_order_project'].browse(active_ids)

        for project in project_ids:
            if project.state != 'maintain':
                raise UserError(_("Selected project cannot be check as they are not in 'maintain' state"))
            project.state = 'check'
            project.start_inspect_time = datetime.datetime.utcnow() # fields.Datetime.now()
            for manhour_manage in project.manhour_manage_ids:
                manhour_manage.real_end_time = datetime.datetime.utcnow() # fields.Datetime.now()

        return {'type': 'ir.actions.act_window_close'}


class WizardProjectBatchCheckPass(models.TransientModel):  # 保养项目_批量_检验通过
    _name = "wizard_project_batch_check_pass"

    @api.multi
    def confirm(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        project_ids = self.env['warranty_order_project'].browse(active_ids)

        for i in project_ids:
            if i.state != 'check':
                raise UserError(_("Selected project cannot be check as they are not in 'check' state"))
            i.state = 'complete'
            i.inspect_result = 'qualified'
            i.end_inspect_time = datetime.datetime.utcnow() # fields.Datetime.now()
            i.vehicle_id.state = 'normal'
            if all(project.state == 'complete' for project in i.warranty_order_id.project_ids):
                i.warranty_order_id.state = 'done'
                # i.warranty_order_id.plan_order_ids.state = 'done'
                for item in i.warranty_order_id.plan_order_ids:
                    item.state = 'done'
                plan = i.warranty_order_id.plan_order_ids[0].parent_id
                if all(plan_sheet.state == 'done' for plan_sheet in plan.plan_order_ids):
                    plan.state = 'done'

        return {'type': 'ir.actions.act_window_close'}
