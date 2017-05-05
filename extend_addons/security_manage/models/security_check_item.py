# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class security_check_item(models.Model):
    _name = 'security_manage.check_item'
    name = fields.Char(string='', default=_('check_info'))
    check_id = fields.Char(string=_('check_id'), required=True)
    check_item_name = fields.Char(string=_('check_item_name'), required=True)
    check_content = fields.Char(string=_('check_content'), required=True)
    check_standards = fields.Char(string=_('check_standards'), required=True)
    form_creator = fields.Many2one('res.users', string=_('form_creator'), required=True, default=lambda
        self: self.env.user)
    create_time = fields.Date(string=_('create_time'), required=True, default=fields.Date.today())

    check_table_id = fields.Many2one('security_manage.check_table',
                                     ondelete='set null')

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
