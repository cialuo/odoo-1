# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Company(models.Model):

    _inherit = "res.company"

    service_ip = fields.Char(default='127.0.0.1')

    service_port = fields.Char(default='8080')

    service_user = fields.Char(default='jasperadmin')

    service_password = fields.Char(default='jasperadmin')

class report_setting(models.TransientModel):

    _name = 'report_setting'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)

    service_ip = fields.Char(related="company_id.service_ip")

    service_port = fields.Char(related="company_id.service_port")

    service_user = fields.Char(related="company_id.service_user")

    service_password = fields.Char(related="company_id.service_password")

    @api.model
    def get_service_url(self):
        """
            获取报表服务器
        :return:
        """
        company_id = self.env.user.company_id
        service_url = "http://%s:%s/jasperserver/flow.html?j_username=%s&amp;j_password=%s" % (
            company_id.service_ip, company_id.service_port, company_id.service_user, company_id.service_password)
        return service_url

    @api.multi
    def execute(self):
        res = super(report_setting, self).execute()
        res = self.env['ir.actions.act_window'].for_xml_id('reports', 'report_config_settings_action')
        return res