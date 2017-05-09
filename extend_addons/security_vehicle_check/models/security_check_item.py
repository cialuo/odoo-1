# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class security_check_item(models.Model):
    _name = 'security_manage.check_item'
    name = fields.Char(string=_('check_id'), required=True)
    check_info = fields.Char(string='', default=_('check_info'))
    check_item_name = fields.Char(string=_('check_item_name'))
    check_content = fields.Char(string=_('check_content'))
    check_standards = fields.Char(string=_('check_standards'))

    create_time = fields.Date(string=_('create_time'), required=True, default=fields.Date.today())

    state = fields.Selection([
        ('use', _('Use')),
        ('archive', _("Archive")),
    ], default='use', string=_('security_check_item_state'))

    @api.multi
    def action_to_default(self):
        self.state = 'use'

    @api.multi
    def action_archive(self):
        self.state = 'archive'
