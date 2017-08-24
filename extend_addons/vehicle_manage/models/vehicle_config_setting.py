#-*- coding: utf8 -*-

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    work_fee = fields.Float(default=50)

    average_day_number = fields.Integer(string='Average Day Number',default=30)

    maintenance_settings = fields.Selection([('control','Control Number'),('uncontrol','UNControl Number')],default='uncontrol',string='maintenance_settings_field')

class VehicleSettings(models.TransientModel):
    _name = 'vehicle.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)
    work_fee = fields.Float(related='company_id.work_fee', default=50)
    average_day_number = fields.Integer(related='company_id.average_day_number', default=30,string='Average Day Number')
    maintenance_settings = fields.Selection(related='company_id.maintenance_settings', default='uncontrol',string='maintenance_settings_field')

    @api.multi
    def execute(self):
        res = super(VehicleSettings, self).execute()
        res = self.env['ir.actions.act_window'].for_xml_id('vehicle_manage', 'action_vehicle_config_settings')
        return res