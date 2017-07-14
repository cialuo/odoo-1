#-*- coding: utf8 -*-

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    work_fee = fields.Float(default=50)


class VehicleSettings(models.TransientModel):
    _name = 'vehicle.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)
    work_fee = fields.Float(related='company_id.work_fee', default=50)

    @api.multi
    def execute(self):
        res = super(VehicleSettings, self).execute()
        res = self.env['ir.actions.act_window'].for_xml_id('vehicle_manage', 'action_vehicle_config_settings')
        return res