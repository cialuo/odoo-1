# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
import datetime
from datetime import timedelta
from odoo.exceptions import UserError

class WarrantyMaintainSheet(models.Model): # 保养单
    _inherit = 'mail.thread'
    _name = 'fleet_warranty_maintain_sheet'
    name = fields.Char(string='Maintain Sheet', required=True, index=True, default='New')

    sequence = fields.Integer('Sequence', default=1)

    vehicle_id = fields.Many2one('fleet.vehicle', string="VehicleNo", required=True, )  # 车号

    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id', store=True, readonly=True)  # 车型

    license_plate = fields.Char("License Plate", related='vehicle_id.license_plate', store=True, readonly=True)  # 车牌


    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    report_repair_user = fields.Many2one('hr.employee', string="Report Name", default=_default_employee, required=True) # 报修人

    operating_mileage = fields.Float(digits=(6, 1), string="OM")  # 运营里程

    warranty_category = fields.Many2one('fleet_manage_warranty.category', 'WC', ondelete='cascade', required=True)  # 保养类别

    planned_date = fields.Date('PlannedDate', default=fields.Date.context_today)  # 计划日期

    vin = fields.Char()  # 车架号

    average_daily_kilometer = fields.Float(digits=(6, 1), string="ADK")  # 平均日公里

    line = fields.Char()  # 线路

    repair_unit = fields.Char()  # 承修单位

    repair_workshop = fields.Char()  # 承修车间

    fleet = fields.Char()  # 车队

    maintenance_level = fields.Char()  # 维修等级

    fill_personnel = fields.Char()  # 填单人

    fill_personnel_unit = fields.Char()  # 填单人单位

    remark = fields.Char()  # 备注信息

    maintain_location = fields.Char()  # 保养地点

    state = fields.Selection([ # 状态
        ('draft', "draft"),
        ('dispatch', "dispatch"),
        ('maintain', "maintain"),
        ('inspect', "inspect"),
        ('done', "done"),
    ], default='draft')

    @api.multi
    def action_confirm_effective(self): # 确认生效 生成保养单
        self.ensure_one()
        # for i in self.repair_ids:
        #     if not i.fault_method_id:
        #         raise exceptions.UserError("Maintain Repair Method Required!")
        #         break

        self.state = 'dispatch'
        # for i in self.repair_ids:
        #     if i.state == 'precheck':
        #         i.state = 'dispatch'

        device_lines =[]
        for i in self.vehicle_id.vehicle_device_ids:
            vals = {
                'device_id': i.device_id.id,
                'serial_no': i.serial_no,
                'name': i.name,
                'fixed_asset_number': i.fixed_asset_number,
                'create_date_ext': i.create_date_ext,
            }
            device_lines.append([0, 0, vals])

        vals = {
            "name": "JJD_"+self.name,
            "maintain_sheet": self.id,
            "vehicle_id": self.vehicle_id.id,
            'device_ids':device_lines
        }
        handover_sheet = self.env['fleet_warranty_handover_sheet'].search([("maintain_sheet", '=', self.id)])
        if not handover_sheet:
            self.env['fleet_warranty_handover_sheet'].create(vals)





    picking_ids = fields.One2many("stock.picking", 'maintainsheet_id', string='Stock Pickings')

    @api.multi
    def create_get_picking(self): # 创建领料单
        self.ensure_one()
        context = dict(self.env.context,
            default_maintainsheet_id=self.id,
            default_origin=self.name,
            default_picking_type_id=self.env.ref('stock_picking_types.picking_type_picking_material').id,
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
        context = dict(self.env.context,
            default_maintainsheet_id=self.id,
            default_origin=self.name,
            default_picking_type_id=self.env.ref('stock_picking_types.picking_type_return_material').id,
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
    def action_into_maintain(self):  # 保养单 进入保养状态
        # self.ensure_one()
        # self.state = 'maintain'
        # for item in self.item_ids:
        #     if item.state == 'dispatch':
        #         item.state = 'maintain'

        """
        维修单:
            功能：开工
            状态：待修->维修
            更新工时管理的实际开工时间
        """
        self.ensure_one()
        if not self.manhour_manage_ids:
            raise exceptions.UserError(_("Maintain Repair Jobs Required!"))
        self.write({'state': 'maintain'})

        for i in self.manhour_manage_ids:
            i.real_start_time = datetime.datetime.utcnow()
        for item in self.item_ids:
            item.state = 'maintain'

        import_products = self.mapped('available_product_ids').filtered(lambda x: x.change_count > 0 and x.product_id.is_important)
        no_import_products = self.mapped('available_product_ids').filtered(lambda x: x.change_count > 0 and not x.product_id.is_important)
        picking_type = self.env.ref('stock_picking_types.picking_type_issuance_of_material')

        location_id = self.env.ref('stock.stock_location_stock').id # 库存
        location_dest_id = self.env.ref('stock_picking_types.stock_location_ullage').id # 维修(生产)虚位
        if import_products:
            location_dest_id = self.vehicle_id.location_stock_id.id # 随车实位

        for products in [import_products, no_import_products]:
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
                }
                move_lines.append((0, 0, vals))
            if move_lines:
                picking = self.env['stock.picking'].create({
                    'origin': self.name,
                    'location_id': location_id,
                    'location_dest_id': location_dest_id,
                    'picking_type_id': picking_type.id,
                    'maintainsheet_id': self.id,
                    'move_lines': move_lines
                })
            if picking:
                picking.action_confirm()

    @api.multi
    def action_into_inspect(self):  # 保养单 全部报检
        self.ensure_one()
        if not self.manhour_manage_ids:
            raise exceptions.UserError(_("Manhour Manage Ids Required!"))
        self.write({'state': 'inspect'})

        for i in self.manhour_manage_ids:
            i.real_end_time = datetime.datetime.utcnow()
        for item in self.item_ids:
            item.state = 'check'

    @api.multi
    def action_manage_handover_sheet(self):  # 管理交接单
        self.ensure_one()
        maintain_sheet = self.env['fleet_warranty_handover_sheet'].search([("maintain_sheet", '=', self.id)])
        action = self.env.ref('fleet_manage_warranty_maintain.fleet_warranty_handover_sheet_action').read()[0]
        action['res_id'] = maintain_sheet.id  # [('id', '=', deliverys.id)]
        action['views'] = [(self.env.ref('fleet_manage_warranty_maintain.fleet_warranty_handover_sheet_view_form').id, 'form')]
        return action



    # @api.multi
    # def action_draft(self):
    #     self.state = 'draft'
    #
    # @api.multi
    # def action_confirm(self):
    #     self.state = 'confirmed'
    #
    # @api.multi
    # def action_done(self):
    #     self.state = 'done'



    plan_id = fields.Many2one('fleet_warranty_plan', 'planId', required=True, ondelete='cascade')  # 车辆保养计划ID

    item_ids = fields.One2many('fleet_warranty_sheet_item', 'maintainsheet_id', 'maintainsheetId') # 保养项目

    manhour_manage_ids = fields.One2many('fleet_warranty_manhour_manage', 'maintainsheet_id', 'maintainsheetId') # 工时管理

    available_product_ids = fields.One2many('fleet_warranty_available_product', 'maintainsheet_id', 'maintainsheetId') # 可领物料

    instruction_ids = fields.One2many('fleet_warranty_sheet_instruction', 'maintainsheet_id', 'maintainsheetId') # 作业指导

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('warranty_plan.order') or 'New'

        # # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        # if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
        #     partner = self.env['res.partner'].browse(vals.get('partner_id'))
        #     addr = partner.address_get(['delivery', 'invoice'])
        #     vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
        #     vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
        #     vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)

        result = super(WarrantyMaintainSheet, self.with_context(mail_create_nolog=True)).create(vals)
        result.message_post(body=_('%s has been added to the maintain sheet!') % (result.name,))
        return result

    def if_complete_dispatch(self):
        print 'complete_dispatch!!!!'
        total_manhour = sum([manhour.percentage_work for manhour in self.manhour_manage_ids])
        sum_manhour = len(self.item_ids)*100
        if total_manhour == sum_manhour:
            return True
        elif total_manhour > sum_manhour:
            raise exceptions.ValidationError(_('this "percentage_work" may not be Incorrect'))

    # @api.multi
    # def write(self, vals):
    #     print 'write!!!!'
    #     if self.state == 'dispatch':
    #         if self.if_complete_dispatch():
    #             print 'done!!!!'
    #             for manhour in self.manhour_manage_ids:
    #                 manhour.real_start_time = datetime.datetime.utcnow()
    #             for item in self.item_ids:
    #                 item.state = 'maintain'
    #             vals['state'] = 'maintain'
    #
    #     result = super(WarrantyMaintainSheet, self).write(vals)
    #     return result


    @api.multi
    def action_batch_dispatch(self): # 批量派工
        # if any(expense.state != 'draft' for expense in self):
        #     raise UserError(_("You cannot report twice the same line!"))
        # if len(self.mapped('employee_id')) != 1:
        #     raise UserError(_("You cannot report expenses for different employees in the same report!"))
        # print self.id
        return {
            'name': 'Batch Dispatch',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'fleet_warranty_wizard_dispatch', # 'res_model': 'hr.expense.sheet',
            # 'id':'batch_dispatch_view_form',
            'context': {
                # 'default_sheetId': self.id
                # 'default_name': self.id
                # 'default_expense_line_ids': [line.id for line in self],
                # 'default_employee_id': self[0].employee_id.id,
                # 'default_name': 'mingger' # self[0].name if len(self.ids) == 1 else ''
            },
            'view_id': self.env.ref('fleet_manage_warranty_maintain.wizard_dispatch_form').id,
            # 'target': 'current',
            'target': 'new'
            # 'res_id': self.id, # self.env.context.get('cashbox_id')
        }

    # @api.onchange('manhour_manage_ids')
    # def on_change_manhour_manage_ids(self):
    #     print 'on_change_manhour_manage_ids'
    #     for item in self.item_ids:
    #         manhour_percentage_work=0
    #         for manhour_manage in item.manhour_manage_ids:
    #             manhour_percentage_work += manhour_manage.percentage_work
    #         item.percentage_work = 100 - manhour_percentage_work


class MaintainSheetItem(models.Model): # 保养单_保养项目
    _name = 'fleet_warranty_sheet_item'
    _order = "sequence"
    #_rec_name = "product_id"


    name = fields.Char(related='item_id.name') # related='item_id.name', store=True

    sequence = fields.Integer('Sequence', default=1)

    maintainsheet_id = fields.Many2one('fleet_warranty_maintain_sheet', index=True) # 所属保养单

    category_id = fields.Many2one('fleet_manage_warranty.category') # 保养类别

    item_id = fields.Many2one('fleet_manage_warranty.item', 'Item', required=True) # 保养项目

    important_product_id = fields.Many2one('product.product', related='item_id.important_product_id',string="Important Product")

    maintenance_mode = fields.Many2one('fleet_manage_warranty.mode', 'Maintenance Mode', related='item_id.mode')  # 保修方式

    vehicle_id = fields.Many2one('fleet.vehicle', related='maintainsheet_id.vehicle_id')  # 车号

    vehicle_type = fields.Many2one("fleet.vehicle.model", related='maintainsheet_id.vehicle_id.model_id')  # 车型

    license_plate = fields.Char("License Plate", related='maintainsheet_id.vehicle_id.license_plate')  # 车牌



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
    ], default='nodispatch')

    inspection_operation = fields.Selection([ # 报检操作
        ('noinspection', ""),
        ('inspection', "inspection"),
    ], default='noinspection')

    reinspection_count = fields.Integer(string="ReinspectionCount")  # 重检验次数 compute="_compute_count_all", cost_count =

    work_time = manhour = fields.Float(digits=(6, 1)) # 工时定额 # fields.Integer('WorkTime') # work_time = fields.Integer(related='fault_method_id.work_time', store=True, readonly=True, copy=False)
    user_id = fields.Many2one('hr.employee', string="Repair Name", ondelete='set null')
    plan_start_time = fields.Datetime("Plan Start Time", default=datetime.datetime.utcnow())
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

    @api.onchange('manhour_manage_ids')
    def on_change_manhour_manage_ids(self):
        manhour_percentage_work = 0
        for manhour_manage in self.manhour_manage_ids:
            manhour_percentage_work += manhour_manage.percentage_work
        self.percentage_work = 100-manhour_percentage_work

    # bol_select = fields.Boolean("Bol Select")


    component_ids = fields.Many2many('product.component', 'fleet_warranty_sheet_item_component_rel', 'item_component_id', 'component_id', 'Component',
        readonly=True, domain="[('product_id', '=', important_product_id),('parent_vehicle','=',vehicle_id)]")

    # , states = {
    #     'done': [('readonly', True)],
    #     'inspect': [('readonly', True)],
    #     'repair': [('readonly', True)],
    # }

    manhour_manage_ids = fields.One2many("fleet_warranty_manhour_manage", 'item_id', string='ManhourManageIds')

    @api.multi
    def dispatch(self):         #派工
        self.ensure_one()
        if not self.user_id:
            raise exceptions.UserError("user_id Required!")

        manhour_percentage_work = 0
        for manhour_manage in self.manhour_manage_ids:
            manhour_percentage_work += manhour_manage.percentage_work

        print manhour_percentage_work

        percentage_work=self.percentage_work+manhour_percentage_work

        print percentage_work

        if percentage_work < 0 or percentage_work > 100:
            raise exceptions.ValidationError(_('"percentage_work" may not be Incorrect'))


        # self_work = self.percentage_work * self.work_time / 100

        vals = {
            "plan_start_time": self.plan_start_time,
            "plan_end_time": self.plan_end_time,
            "work_time": self.work_time,
            "percentage_work": self.percentage_work,
            # 'self_work': self_work,
            "user_id":self.user_id.id,
            "sequence":len(self.manhour_manage_ids)+1,
            "maintainsheet_id":self.maintainsheet_id.id
        }

        self.percentage_work=100-percentage_work
        self.state = 'dispatch'

        self.write({'manhour_manage_ids': [(0, 0, vals)]})

        total_manhour = sum([manhour.percentage_work for manhour in self.maintainsheet_id.manhour_manage_ids])
        sum_manhour = len(self.maintainsheet_id.item_ids)*100
        if total_manhour == sum_manhour:
            print 'send!'

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.maintainsheet_id.name:
                name = record.maintainsheet_id.name + '/' + name
            res.append((record.id, name))
        return res

        # for record in self:
        #     name = "倚天屠龙"
        # #     name = record.item_id.name
        # return name




class WarrantyManhourManage(models.Model): # 保养单_保养项目_工时管理
    _name = 'fleet_warranty_manhour_manage'
    _order = "sequence"

    name = fields.Char("Job Name", help="Job Name")

    sequence = fields.Integer("Sequence", help="Sequence")

    item_id = fields.Many2one("fleet_warranty_sheet_item", ondelete='cascade',string="Item") # 所属保养项目

    item_category_id = fields.Many2one('fleet_manage_warranty.category', related='item_id.category_id') # 所属保养项目的保养类别

    item_item_id = fields.Many2one('fleet_manage_warranty.item', 'Item', related='item_id.item_id') # 所属保养项目的保养项目

    user_id = fields.Many2one('hr.employee', string="Repair Name", required=True) # 保养人员

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


    @api.depends('real_start_time', 'real_end_time')
    def _get_real_work(self):
        for r in self:
            if not (r.real_start_time and r.real_end_time):
                continue
            start_time = fields.Datetime.from_string(r.real_start_time)
            end_time = fields.Datetime.from_string(r.real_end_time)
            r.real_work = (end_time - start_time).seconds / 60.0



    maintainsheet_id = fields.Many2one('fleet_warranty_maintain_sheet', index=True)


class WarrantyAvailableProduct(models.Model): # 保养单_可领物料
    _name = 'fleet_warranty_available_product'

    sequence = fields.Integer("Sequence", help="Sequence")

    maintainsheet_id = fields.Many2one('fleet_warranty_maintain_sheet', ondelete='set null', string="MaintainsheetId", index=True) # 所属保养单

    category_id = fields.Many2one('fleet_manage_warranty.category') # 保养类别

    item_id = fields.Many2one('fleet_manage_warranty.item', 'Item')  # 保养项目

    product_id = fields.Many2one('product.product', 'Product', required=True) # 物资

    product_code = fields.Char('Product Code', related='product_id.default_code') # 物资编码 , store=True, readonly=True

    categ_id = fields.Many2one('product.category', related='product_id.categ_id',
                               string='Product Category')
    uom_id = fields.Many2one('product.uom', 'Unit of Measure', related='product_id.uom_id')
    onhand_qty = fields.Float('Quantity On Hand', related='product_id.qty_available')
    virtual_available = fields.Float('Forecast Quantity', related='product_id.virtual_available')
    require_trans = fields.Boolean("Require Trans", readonly=True)
    vehicle_model = fields.Many2many(related='product_id.vehicle_model', relation='product_vehicle_model_rec',
                                      string='Suitable Vehicle', readonly=True)
    product_size = fields.Text("Product Size", related='product_id.description', readonly=True)

    change_count = fields.Integer("Change Count")
    max_count = fields.Integer("Max Count")

    # product_name = fields.Char('Product Name', related='product_id.name', store=True, readonly=True) # 物资名称
    #
    # max_available_count = fields.Integer("Max Available Count") # 领用上限
    #
    # default_avail_count = fields.Integer("Default Available Count") # 默认用量
    #
    # stock_count = fields.Integer("Stock Count") # 库存数量
    #
    # available_count = fields.Integer("Available Count") # 可用数
    #
    # post_old_get_new = fields.Boolean("Post Old Get New") # 交旧领新
    #
    # vehicle_type = fields.Many2one("fleet.vehicle.model")  # 适用车型


    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_code = self.product_id.code
            self.product_name = self.product_id.name



class MaintainSheetInstruction(models.Model): # 保养单_作业指导
    _name = 'fleet_warranty_sheet_instruction'
    _order = "sequence"

    sequence = fields.Integer('Sequence', default=1)

    maintainsheet_id = fields.Many2one('fleet_warranty_maintain_sheet', index=True) # 所属保养单

    category_id = fields.Many2one('fleet_manage_warranty.category') # 保养类别

    item_id = fields.Many2one('fleet_manage_warranty.item', 'Item', required=True) # 保养项目

    maintenance_mode = fields.Many2one('fleet_manage_warranty.mode', 'Maintenance Mode', related='item_id.mode')  # 保修方式

    operational_manual = fields.Text() # 作业手册




class WarrantyInspectSheet(models.Model): # 检验单

    _inherit = 'fleet_warranty_sheet_item'

    inspect_result = fields.Selection([
        ('qualified', 'qualified'), # 合格
        ('defective', 'defective')  # 不合格
    ], string="Inspect Result") # 检验结论

    start_inspect_time = fields.Datetime("Start Inspect Time") # 报检时间

    end_inspect_time = fields.Datetime("End Inspect Time") # 检验通过时间

    return_record_ids = fields.One2many("fleet_warranty_return_record", 'sheet_item', string='Return Record Ids')

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    inspect_user_id = fields.Many2one('hr.employee', string="Inspect User", default=_default_employee) # 检验员

    rework_count = fields.Integer("Rework Count", help="Rework Count",compute="_get_rework_count") # 重检次数

    inspection_criteria = fields.Text(related='item_id.inspection_criteria')  # 检验标准

    item_name = fields.Char(related='item_id.name')  # 项目名称

    def _get_rework_count(self): # 获取退检次数
        for i in self:
            i.rework_count = len(i.return_record_ids)

    @api.multi
    def action_into_check(self):  # 进入检验状态
        for item in self:
            item.state = 'check'
            item.start_inspect_time = fields.Datetime.now()
            for manhour_manage in self.manhour_manage_ids:
                manhour_manage.real_end_time = fields.Datetime.now()

            # for i in self:
            #     if i.state not in ('inspect','done'):
            #         raise exceptions.UserError(_("Selected inspect(s) cannot be confirmed as they are not in 'inspect' state"))
            #     i.state = 'done'
            #     i.inspect_result = 'qualified'
            #     i.end_inspect_time = fields.Datetime.now()
            #
            #     if all(repair.state in ['done'] for repair in i.report_id.repair_ids):
            #         i.report_id.state = 'done'

    @api.multi
    def action_into_maintain(self):  # 进入保养状态
        for item in self:
            item.state = 'maintain'

    @api.multi
    def action_check_pass(self):
        for i in self:
            # if i.state != 'check': # not in ('check','done')
            #     raise exceptions.UserError(_("Selected inspect(s) cannot be confirmed as they are not in 'inspect' state"))
            i.state = 'complete'
            i.inspect_result = 'qualified'
            i.end_inspect_time = fields.Datetime.now()

            if all(item.state == 'complete' for item in i.maintainsheet_id.item_ids):
                i.maintainsheet_id.state = 'done'

    @api.multi
    def action_return(self, reason=''): # 退回重修
        inspect_return_time = fields.Datetime.now()
        vals = {
            "sheet_item": self.id,
            "inspect_return_time": inspect_return_time,
            "return_reason": reason,
            "sequence": len(self.return_record_ids) + 1
        }
        self.write({
            "state":'maintain',
            "end_inspect_time": inspect_return_time,
            "inspect_result": "defective",
            "return_record_ids": [(0, 0, vals)]
        })


class WarrantyReturnRecord(models.Model): # 退检记录
    _name = 'fleet_warranty_return_record'

    sheet_item = fields.Many2one('fleet_warranty_sheet_item', string="Sheet Item")

    maintainsheet_name = fields.Char(string='Maintainsheet Name', related='sheet_item.maintainsheet_id.name')

    inspect_user_id = fields.Many2one('hr.employee', related='sheet_item.inspect_user_id', string="Inspect User")

    maintenance_personnel = fields.Char(string='Maintenance Personnel',related='sheet_item.maintenance_personnel')

    # fault_method_id = fields.Many2one("fleet_manage_fault.method", related='repair_id.fault_method_id',
    #                                   ondelete='set null', string="Fault Method")

    return_reason = fields.Text("Return Reason")

    inspect_return_time = fields.Datetime("Inspect Return Time")

    sequence = fields.Integer("Sequence")




class WarrantyWizardDispatch(models.TransientModel): # 批量派工
    _name = 'fleet_warranty_wizard_dispatch'

    def _default_sheetId(self):
        active_id = self._context.get('active_id')
        return active_id

    sheetId=fields.Char(default=_default_sheetId)

    def _default_item(self):
        active_id=self._context.get('active_id')
        maintain_sheet = self.env['fleet_warranty_maintain_sheet'].search([('id', '=', active_id)])
        item_ids=maintain_sheet.item_ids.search([('maintainsheet_id', '=', active_id), ('state', '=', 'nodispatch')])
        return item_ids

    item_id = fields.Many2many('fleet_warranty_sheet_item', string='Item', required=True) # , default=_default_item

    def _default_user(self):
        employees = self.env['hr.employee'].browse([16, 5, 1])
        return employees

    user_id = fields.Many2many('hr.employee', string="User", required=True) # , default=_default_user

    @api.multi
    def batch_dispatch_manhour(self):
        sheetId = self._context.get('active_id')

        maintain_sheet = self.env['fleet_warranty_maintain_sheet'].search([('id', '=', sheetId)])
        manhours=[]
        manhour_count=len(maintain_sheet.manhour_manage_ids)

        user_count=len(self.user_id)
        #
        # sum_manhour_percentage_work=sum(maintain_sheet.manhour_manage_ids.mapped('percentage_work'))
        #
        #
        # if sum_manhour_percentage_work > 0 and sum_manhour_percentage_work < 100:
        #     val_manhour_percentage_work=(100-sum_manhour_percentage_work)/user_count
        # else:
        #     val_manhour_percentage_work=100/user_count

        for item in self.item_id:
            sum_manhour_percentage_work = sum(item.manhour_manage_ids.mapped('percentage_work'))

            if sum_manhour_percentage_work == 100:
                continue

            val_manhour_percentage_work = 0

            if sum_manhour_percentage_work > 0 and sum_manhour_percentage_work < 100:
                val_manhour_percentage_work = (100 - sum_manhour_percentage_work) / user_count
            else:
                val_manhour_percentage_work = 100 / user_count

            # self_work = val_manhour_percentage_work * item.work_time / 100

            for user in self.user_id:
                manhour_count+=1

                plan_start_time = datetime.datetime.utcnow()
                plan_end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=item.work_time * 60)

                manhour = {
                    'name': manhour_count,
                    'sequence': manhour_count,
                    'item_id': item.id,
                    'user_id': user.id,
                    'plan_start_time': plan_start_time,
                    'plan_end_time': plan_end_time,
                    'work_time': item.work_time,
                    'percentage_work': val_manhour_percentage_work,
                    # 'self_work': self_work,
                    'maintainsheet_id':sheetId
                }
                manhours.append((0, 0, manhour))
            item.update({
                'state': 'dispatch',
                'percentage_work':100-(sum_manhour_percentage_work+val_manhour_percentage_work*user_count)
            })
        maintain_sheet.write({'manhour_manage_ids': manhours})

        return False




class WarrantyWizardInspectReturn(models.TransientModel): # 退回重修
    _name = "fleet_warranty_sheet_inspect_return"
    # _description = "Confirm return"

    return_reason = fields.Text("Return Reason")

    @api.multi
    def inspect_return(self):
        context = dict(self._context or {})
        # print context
        active_id = context.get('active_id', '') or ''
        record = self.env['fleet_warranty_sheet_item'].browse(active_id)
        if record.state != 'check':
            raise UserError(_("Selected item cannot be return as they are not in 'check' state."))
        record.action_return(self.return_reason)
        return {'type': 'ir.actions.act_window_close'}