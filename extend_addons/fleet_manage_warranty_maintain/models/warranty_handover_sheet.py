# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyHandoverSheet(models.Model): # 交接单
    _name = 'fleet_warranty_handover_sheet'

    name = fields.Char(string="Handover Sheet", required=True, index=True, default='New')

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

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet_warranty_handover_sheet') or '/'
        return super(WarrantyHandoverSheet, self).create(vals)

    @api.multi
    def action_delivery(self):
        self.state = 'delivery'
        self.delivery_time = fields.Datetime.now()

    @api.multi
    def action_delivery_return(self):
        self.state = 'delivery_return'
        self.delivery_return_time = fields.Datetime.now()

