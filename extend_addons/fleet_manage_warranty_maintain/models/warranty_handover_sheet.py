# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class WarrantyHandoverSheet(models.Model): # 交接单
    _inherit = 'mail.thread'
    _name = 'fleet_warranty_handover_sheet'

    name = fields.Char(string="JJD", required=True, index=True, default='New')

    branch_office = fields.Char() # 分公司

    maintain_sheet = fields.Many2one("fleet_warranty_maintain_sheet", ondelete='cascade') # 所属保养单

    vehicle_id = fields.Many2one('fleet.vehicle', string="VehicleNo", required=True, )  # 车号

    driver = fields.Char() # 驾驶员

    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id', store=True, readonly=True)  # 车型

    license_plate = fields.Char("License Plate", related='vehicle_id.license_plate', store=True, readonly=True)  # 车牌

    create_sheet_user = fields.Many2one('hr.employee', related='maintain_sheet.report_repair_user', string="Create Sheet User") # 建单人

    delivery_time = fields.Datetime("Delivery Time") # 交接时间

    delivery_return_time = fields.Datetime("Delivery Return Time") # 交回时间

    driver = fields.Char() # 驾驶员

    maintenance_personnel = fields.Char() # 机务员

    commitment_unit = fields.Char() # 承接单位

    state = fields.Selection([
        ('draft', "Draft"),
        ('delivery', "Delivery"),
        ('delivery_return', "Delivery Return"), ], default='draft')

    device_ids = fields.One2many('fleet_warranty_handover_maintenance', 'delivery_id', string='Device Ids')

    device_return_ids = fields.One2many('fleet_warranty_handover_return_maintenance', 'delivery_id', string='Device Return Ids')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet_warranty_handover_sheet') or '/'

        result = super(WarrantyHandoverSheet, self.with_context(mail_create_nolog=True)).create(vals)
        result.message_post(body=_('%s has been added to the handover_sheet!') % (result.name,))
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
        for i in self.device_ids:
            vals = {
                'device_id': i.device_id.id,
                'serial_no': i.serial_no,
                'name': i.name,
                'fixed_asset_number': i.fixed_asset_number,
                'create_date_ext': i.create_date_ext,
            }
            device_lines.append([0, 0, vals])
        self.device_return_ids = device_lines

    @api.multi
    def action_to_open(self): # 交接单跳转到维修单
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('fleet_manage_warranty_maintain', xml_id)
            res.update(
                # context=dict(self.env.context, default_id=self.maintain_sheet.id),
                domain=[('id', '=', self.maintain_sheet.id)]
            )
            return res
        return False


class WarrantyHandoverMaintainDevice(models.Model): # 交接清单
    _name = 'fleet_warranty_handover_maintenance'

    delivery_id = fields.Many2one('fleet_warranty_handover_sheet', ondelete='cascade', string="Vehicle")
    device_id = fields.Many2one('maintenance.equipment', string="Equipment")
    serial_no = fields.Char("Serial No", help="Serial No")
    name = fields.Char("Name", help="Name")
    fixed_asset_number = fields.Char("Fixed Asset Number", help="Fixed Asset Number")
    create_date_ext = fields.Datetime("Create Date", help="Create Date")


class WarrantyHandoverMaintainDevice(models.Model): # 交回清单
    _name = 'fleet_warranty_handover_return_maintenance'

    delivery_id = fields.Many2one('fleet_warranty_handover_sheet', ondelete='cascade', string="Vehicle")
    device_id = fields.Many2one('maintenance.equipment', string="Equipment")
    serial_no = fields.Char("Serial No", help="Serial No")
    name = fields.Char("Name", help="Name")
    fixed_asset_number = fields.Char("Fixed Asset Number", help="Fixed Asset Number")
    create_date_ext = fields.Datetime("Create Date", help="Create Date")

