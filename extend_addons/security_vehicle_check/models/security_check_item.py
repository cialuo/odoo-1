# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class security_check_item(models.Model):
    _name = 'security_manage.check_item'
    name = fields.Char(string='check_id', required=True)
    check_info = fields.Char(default="检查信息")
    check_item_name = fields.Char(string='check_item_name')
    check_content = fields.Char(string='check_content')
    check_standards = fields.Char(string='check_standards')

    create_time = fields.Date(string='create_time', required=True, default=fields.Date.today())

    state = fields.Selection([
        ('use', 'Use'),
        ('archive', "Archive"),
    ], default='use', string='security_check_item_state')

    @api.multi
    def action_to_default(self):
        self.state = 'use'

    @api.multi
    def action_archive(self):
        self.state = 'archive'
