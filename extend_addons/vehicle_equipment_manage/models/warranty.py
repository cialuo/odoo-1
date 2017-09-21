# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import timedelta

class WarrantyOrder(models.Model): # 保养单
    _inherit = 'warranty_order'

    @api.multi
    def action_confirm_effective(self):  # 确认生效 生成保养单
        res = super(WarrantyOrder, self).action_confirm_effective()

        device_lines =[]
        for i in self.vehicle_id.equipment_ids:
            vals = {
                'equipment_id': i.equipment_id.id,
                'serial_no': i.serial_no,
                # 'name': i.name,
                'fixed_asset_number': i.fixed_asset_number,
                'create_date_ext': i.create_date_ext,
            }
            device_lines.append([0, 0, vals])

        vals = {
            "name": "JJD_"+self.name,
            "warranty_order_id": self.id,
            "vehicle_id": self.vehicle_id.id,
            'list_ids':device_lines
        }
        handover_sheet = self.env['warranty_handover_order'].search([("warranty_order_id", '=', self.id)])
        if not handover_sheet:
            self.env['warranty_handover_order'].create(vals)
        return res


    @api.multi
    def action_manage_handover_sheet(self):  # 管理交接单
        self.ensure_one()
        warranty_order_id = self.env['warranty_handover_order'].search([("warranty_order_id", '=', self.id)])
        action = self.env.ref('vehicle_equipment_manage.warranty_handover_order_action').read()[0]
        action['res_id'] = warranty_order_id.id
        action['views'] = [(self.env.ref('vehicle_equipment_manage.warranty_handover_order_form').id, 'form')]
        return action


class WarrantyHandoverOrder(models.Model): # 交接单
    _inherit = 'mail.thread'
    _name = 'warranty_handover_order'

    name = fields.Char(string="JJD", required=True, index=True, default='/')

    branch_office = fields.Char(string="Branch Office") # 分公司

    warranty_order_id = fields.Many2one("warranty_order", ondelete='cascade') # 所属保养单

    vehicle_id = fields.Many2one('fleet.vehicle', string="VehicleNo", required=True, )  # 车号

    driver = fields.Char(string="Driver") # 驾驶员

    vehicle_type = fields.Many2one("fleet.vehicle.model", string="Vehicle Model", related='vehicle_id.model_id', store=True, readonly=True)  # 车型

    license_plate = fields.Char("License Plate", related='vehicle_id.license_plate', store=True, readonly=True)  # 车牌

    create_sheet_user = fields.Many2one('hr.employee', related='warranty_order_id.report_repair_user', string="Create Sheet User") # 建单人

    delivery_time = fields.Datetime("Delivery Time") # 交接时间

    delivery_return_time = fields.Datetime("Delivery Return Time") # 交回时间

    maintenance_personnel = fields.Char(string="Operator") # 机务员

    commitment_unit = fields.Char(string="Commitment Unit") # 承接单位

    state = fields.Selection([
        ('draft', "Draft"),
        ('delivery', "Delivery"),
        ('delivery_return', "Delivery Return"), ], default='draft', string="MyState")

    list_ids = fields.One2many('warranty_handover_list', 'handover_order_id', string='List Ids') # 交接清单

    back_list_ids = fields.One2many('warranty_handover_back_list', 'handover_order_id', string='Back List Ids') # 交回清单

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('warranty_handover_order') or '/'

        result = super(WarrantyHandoverOrder, self.with_context(mail_create_nolog=True)).create(vals)
        result.message_post(body=_('%s has been added to the handover_order!') % (result.name,))
        return result

    @api.multi
    def action_delivery(self):
        self.state = 'delivery'
        self.delivery_time = fields.Datetime.now()

    @api.multi
    def action_delivery_return(self):
        # self.state = 'delivery_return'
        # self.delivery_return_time = fields.Datetime.utcnow()

        self.state = 'delivery_return'
        self.delivery_return_time = fields.Datetime.now()
        device_lines = []
        for i in self.list_ids:
            vals = {
                'equipment_id': i.equipment_id.id,
                'serial_no': i.serial_no,
                'name': i.name,
                'fixed_asset_number': i.fixed_asset_number,
                'create_date_ext': i.create_date_ext,
            }
            device_lines.append([0, 0, vals])
        self.back_list_ids = device_lines

    @api.multi
    def action_to_open(self): # 交接单跳转到维修单
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('vehicle_warranty', xml_id)
            res.update(
                # context=dict(self.env.context, default_id=self.warranty_order_id.id),
                domain=[('id', '=', self.warranty_order_id.id)]
            )
            return res
        return False


class WarrantyHandoverList(models.Model): # 交接清单
    _name = 'warranty_handover_list'

    handover_order_id = fields.Many2one('warranty_handover_order', ondelete='cascade', string="warranty_handover_order")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")
    serial_no = fields.Char("Serial No", help="Serial No")
    name = fields.Char("Name", help="Name")
    fixed_asset_number = fields.Char("Fixed Asset Number", help="Fixed Asset Number")
    create_date_ext = fields.Datetime("Create Date", help="Create Date")


class WarrantyHandoverBackList(models.Model): # 交回清单
    _name = 'warranty_handover_back_list'

    handover_order_id = fields.Many2one('warranty_handover_order', ondelete='cascade', string="Vehicle")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")
    serial_no = fields.Char("Serial No", help="Serial No")
    name = fields.Char("Name", help="Name")
    fixed_asset_number = fields.Char("Fixed Asset Number", help="Fixed Asset Number")
    create_date_ext = fields.Datetime("Create Date", help="Create Date")
