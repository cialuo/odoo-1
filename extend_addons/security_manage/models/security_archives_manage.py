# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
class archives_class_manage(models.Model):
    _name = 'security_manage.cls_manage'
    name = fields.Char(string=_('archives_class_manage_item_name'))
    item_id = fields.Char(string=_('archives_class_manage_item_id'))
    item_name = fields.Char(string=_('archives_class_manage_table'),default=_('archives_class_manage_table'))
    class_name = fields.Char(string=_('archives_class_manage_class_name'))
    # TODO 这是一个Many2one
    # class_type = fields.Char(string=_('archives_class_manage_class_type'))
    class_type = fields.Selection([
        ('big_class', _('Big class')),
        ('little_class', _('Little class'))
    ], string=_('archives_class_manage_class_type'))

    # TODO 这是一个Many2one
    parent = fields.Char(string=_('archives_class_manage_parent'))

    # form_creator= fields.Char()
    form_creator =  fields.Many2one('res.users',string=_('archives_class_manage_form_creator'),required=True, default=lambda
        self: self.env.user)

    create_time = fields.Date(string=_('archives_class_manage_create_time'))

    state = fields.Selection([
        ('use', _('Use')),
        ('archive', _("Archive")),
    ], default='use', string=_('archives_class_manage_state'))

    @api.multi
    def action_to_default(self):
        self.state = 'use'

    @api.multi
    def action_archive(self):
        self.state = 'archive'
    @api.onchange
    def onTypeChange(self):
        pass