# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import datetime
from datetime import timedelta

class WarrantyMaintainSheet(models.Model): # 保养单
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
    def action_confirm_effective(self): # 确认生效
        self.ensure_one()
        # for i in self.repair_ids:
        #     if not i.fault_method_id:
        #         raise exceptions.UserError("Maintain Repair Method Required!")
        #         break

        self.state = 'dispatch'
        # for i in self.repair_ids:
        #     if i.state == 'precheck':
        #         i.state = 'dispatch'
        vals = {
            "name": "JJD_"+self.name,
            "maintain_sheet": self.id,
            "vehicle_id": self.vehicle_id.id
        }
        handover_sheet = self.env['fleet_warranty_handover_sheet'].search([("maintain_sheet", '=', self.id)])
        if not handover_sheet:
            self.env['fleet_warranty_handover_sheet'].create(vals)

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

        result = super(WarrantyMaintainSheet, self).create(vals)
        return result

    @api.multi
    def action_batch_dispatch(self): # 批量派工
        # if any(expense.state != 'draft' for expense in self):
        #     raise UserError(_("You cannot report twice the same line!"))
        # if len(self.mapped('employee_id')) != 1:
        #     raise UserError(_("You cannot report expenses for different employees in the same report!"))
        print self.id
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


class MaintainSheetItem(models.Model): # 保养单_保养项目
    _name = 'fleet_warranty_sheet_item'
    _order = "sequence"
    #_rec_name = "product_id"

    sequence = fields.Integer('Sequence', default=1)

    maintainsheet_id = fields.Many2one('fleet_warranty_maintain_sheet', index=True) # 所属保养单

    category_id = fields.Many2one('fleet_manage_warranty.category') # 保养类别

    item_id = fields.Many2one('fleet_manage_warranty.item', 'Item', required=True) # 保养项目

    maintenance_mode = fields.Many2one('fleet_manage_warranty.mode', 'Maintenance Mode', related='item_id.mode')  # 保修方式

    maintenance_personnel = fields.Char(compute='_get_maintenance_personnel_names')  # 保养人员

    # @api.depends("manhour_manage_ids")
    def _get_maintenance_personnel_names(self):  #获取维修人名字
        for i in self:
            names = set()
            for j in i.manhour_manage_ids:
                names.add(j.user_id.name)
            i.maintenance_personnel = ",".join(list(names))


    state = fields.Selection([ # 状态
        ('nodispatch', "nodispatch"),
        ('dispatch', "dispatch"),
        ('maintain', "maintain"),
        ('check', "check"),
        ('complete', "complete"),
    ], default='nodispatch')

    inspection_operation = fields.Selection([ # 报检操作
        ('noinspection', "noinspection"),
        ('inspection', "inspection"),
    ], default='noinspection')

    reinspection_count = fields.Integer(string="ReinspectionCount")  # 重检验次数 compute="_compute_count_all", cost_count =

    work_time = manhour = fields.Float(digits=(6, 1)) # 工时定额 # fields.Integer('WorkTime') # work_time = fields.Integer(related='fault_method_id.work_time', store=True, readonly=True, copy=False)
    user_id = fields.Many2one('hr.employee', string="Repair Name")
    plan_start_time = fields.Datetime("Plan Start Time", help="Plan Start Time")
    plan_end_time = fields.Datetime("Plan End Time", help="Plan End Time") # ,compute='_get_end_datetime'
    percentage_work = fields.Float(digits=(6, 1))

    # bol_select = fields.Boolean("Bol Select")

    manhour_manage_ids = fields.One2many("fleet_warranty_manhour_manage", 'item_id', string='ManhourManageIds')

    @api.multi
    def dispatch(self):         #派工
        self.ensure_one()
        if not self.user_id:
            raise exceptions.UserError("user_id Required!")

        self.state = 'dispatch'
        vals = {
            # "repair_id": self.id,
            # "fault_category_id": self.fault_category_id.id,
            # "fault_appearance_id": self.fault_appearance_id.id or None,
            # "fault_reason_id": self.fault_reason_id.id,
            # "fault_method_id": self.fault_method_id.id,
            "plan_start_time": self.plan_start_time,
            "plan_end_time": self.plan_end_time,
            "work_time": self.work_time,
            "percentage_work": self.percentage_work,
            "user_id":self.user_id.id,
            "sequence":len(self.manhour_manage_ids)+1,
            "maintainsheet_id":self.maintainsheet_id.id
        }
        self.write({'manhour_manage_ids': [(0, 0, vals)]})


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

    self_work = fields.Float(digits=(6, 1)) # 本人工时

    real_work = fields.Float(digits=(6, 1)) # 实际工时

    maintainsheet_id = fields.Many2one('fleet_warranty_maintain_sheet', index=True)


class WarrantyAvailableProduct(models.Model): # 保养单_可领物料
    _name = 'fleet_warranty_available_product'

    sequence = fields.Integer("Sequence", help="Sequence")

    maintainsheet_id = fields.Many2one('fleet_warranty_maintain_sheet', ondelete='set null', string="MaintainsheetId", index=True) # 所属保养单

    product_id = fields.Many2one('product.product', 'Product', required=True) # 物资

    product_code = fields.Char('Product Code', related='product_id.default_code', store=True, readonly=True) # 物资编码

    product_name = fields.Char('Product Name', related='product_id.name', store=True, readonly=True) # 物资名称

    max_available_count = fields.Integer("Max Available Count") # 领用上限

    default_avail_count = fields.Integer("Default Available Count") # 默认用量

    stock_count = fields.Integer("Stock Count") # 库存数量

    available_count = fields.Integer("Available Count") # 可用数

    post_old_get_new = fields.Boolean("Post Old Get New") # 交旧领新

    # meet_vehicle_type = fields.Char("Meet Vehicle Type", help="Meet Vehicle Type") # 适用车型

    vehicle_type = fields.Many2one("fleet.vehicle.model")  # 适用车型

    category_id = fields.Many2one('fleet_manage_warranty.category') # 保养类别

    # item_id = fields.Many2one('fleet_manage_warranty.item', 'Item') # 保养项目

    item_id = fields.Many2one('fleet_manage_warranty.item', 'Item')  # 保养项目
    # item_id = fields.Many2one("fleet_warranty_sheet_item", ondelete='cascade',string="Item") # 所属保养项目

    # item_category_id = fields.Many2one('fleet_manage_warranty.category', related='item_id.category_id') # 所属保养项目的保养类别

    # item_item_id = fields.Many2one('fleet_manage_warranty.item', 'Item', related='item_id.item_id') # 所属保养项目的保养项目


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


class WarrantyWizardDispatch(models.TransientModel):
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
        # return False # {}
        sheetId = self._context.get('active_id')

        maintain_sheet = self.env['fleet_warranty_maintain_sheet'].search([('id', '=', sheetId)])
        manhours=[]
        manhour_count=len(maintain_sheet.manhour_manage_ids)

        user_count=len(self.user_id)

        sum_manhour_percentage_work=sum(maintain_sheet.manhour_manage_ids.mapped('percentage_work'))
        print sum_manhour_percentage_work

        val_manhour_percentage_work=0

        if sum_manhour_percentage_work > 0 and sum_manhour_percentage_work < 100:
            val_manhour_percentage_work=(100-sum_manhour_percentage_work)/user_count
        else:
            val_manhour_percentage_work=100/user_count

        print val_manhour_percentage_work

        # current_date_str = fields.Date.context_today(self)
        # current_date = fields.Date.from_string(fields.Date.context_today(self))

        for item in self.item_id:
            for user in self.user_id:
                manhour_count+=1
                print item.work_time

                # duration = timedelta(seconds=item.work_time * 60)
                # plan_end_time = current_date + duration

                plan_start_time = datetime.datetime.utcnow()
                plan_end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=item.work_time * 60)
                self_work = val_manhour_percentage_work*item.work_time/100

                manhour = {
                    'name': manhour_count,
                    'sequence': manhour_count,
                    'item_id': item.id,
                    'user_id': user.id,
                    'plan_start_time': plan_start_time,
                    'plan_end_time': plan_end_time,
                    'work_time': item.work_time,
                    'percentage_work': val_manhour_percentage_work,
                    'self_work': self_work,
                    'maintainsheet_id':sheetId
                }
                # self.env['fleet_warranty_manhour_manage'].create(manhour)
                manhours.append((0, 0, manhour))
            item.update({
                'state': 'dispatch',
            })
        maintain_sheet.write({'manhour_manage_ids': manhours})

        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'fleet_warranty_wizard_dispatch', # 'res_model': 'hr.expense.sheet',
        #     # 'id':'batch_dispatch_view_form',
        #     'context': {
        #         # 'default_expense_line_ids': [line.id for line in self],
        #         # 'default_employee_id': self[0].employee_id.id,
        #         # 'default_name': 'mingger' # self[0].name if len(self.ids) == 1 else ''
        #     },
        #     'res_id': self.copy().id,
        #     'context': self.env.context,
        #     'view_id': self.env.ref('fleet_manage_warranty_maintain.wizard_form_view').id,
        #     # 'target': 'current',
        #     'target': 'new'
        #     # 'res_id': self.id, # self.env.context.get('cashbox_id')
        # }

        return False


