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