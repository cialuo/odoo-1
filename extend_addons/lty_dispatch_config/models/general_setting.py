#-*- coding: utf8 -*-

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    work_fee = fields.Float(default=50)


class General_setting(models.TransientModel):
    _name = 'general.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)
    work_fee = fields.Float(related='company_id.work_fee', default=50)

    @api.multi
    def execute(self):
        res = super(General_setting, self).execute()
        res = self.env['ir.actions.act_window'].for_xml_id('lty_dispatch_config', 'action_general_config_settings')
        return res