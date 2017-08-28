# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Company(models.Model):

    _inherit = "res.company"

    service_ip = fields.Char(default='127.0.0.1')

    service_port = fields.Char(default='8080')

    service_user = fields.Char(default='jasperadmin')

    service_password = fields.Char(default='jasperadmin')

    service_url = fields.Char()

class report_setting(models.TransientModel):

    _name = 'report_setting'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)

    service_ip = fields.Char(related="company_id.service_ip")

    service_port = fields.Char(related="company_id.service_port")

    service_user = fields.Char(related="company_id.service_user")

    service_password = fields.Char(related="company_id.service_password")

    service_url = fields.Char(related="company_id.service_url",compute="_compute_service_url")

    @api.depends('service_ip', 'service_port','service_user','service_password')
    def _compute_service_url(self):

        """
            计算报表服务器的url
            http:// ip : port /jasperserver/flow.html?j_username= service_user &amp;j_password= service_password
        :return:
        """

        self.service_url = "http://%s:%s/jasperserver/flow.html?j_username=%s&amp;j_password=%s" % (self.service_ip,self.service_port,self.service_user,self.service_password)





    @api.multi
    def execute(self):
        res = super(report_setting, self).execute()
        res = self.env['ir.actions.act_window'].for_xml_id('reports', 'action_report_setting')
        return res