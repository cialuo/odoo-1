# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class security_check_item(models.Model):
    _name = 'security_manage.security_check_item'
    name = fields.Char(string=_('check_info'))
    check_id = fields.Char(string=_('check_id'))
    check_item_name = fields.Char(string=_('check_item_name'))
    check_content = fields.Char(string=_('check_content'))
    check_standards = fields.Char(string=_('check_standards'))
    form_creator = fields.Char(string=_('form_creator'))
    create_time = fields.Date(string=_('create_time'))

    check_table_id = fields.Many2one('security_manage.security_check_table',
                                     ondelete='restrict')

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


class security_check_table(models.Model):
    _name = 'security_manage.security_check_table'
    name = fields.Char(string=_('check_table'))
    check_table_id = fields.Char(string=_('check_table_id'))
    function_module = fields.Char(string=_('function_module'))
    remarks = fields.Char(string=_('remarks'))
    check_type = fields.Char(string=_('check_type'))
    # TODO many2one
    responser = fields.Char(string=_('check_responser'))
    # TODO many2one
    parent_company = fields.Char(string=_('check_parent_company'))

    plan_detail = fields.One2many('security_manage.security_check_item', 'check_table_id', string=_('plan_detail'))

    state = fields.Selection([
        ('draft', _('Draft_check_table')),
        ('execute', _('Execute_check_table')),
        ('archive', _("Archive_check_table")),
    ], default='draft', string=_('security_check_table_state'))

    @api.multi
    def action_to_draft(self):
        self.state = 'draft'

    @api.multi
    def action_execute(self):
        self.state = 'execute'

    @api.multi
    def action_archive(self):
        self.state = 'archive'


class archives_class_manage(models.Model):
    _name = 'security_manage.archives_class_manage'
    name = fields.Char(string=_('archives_class_manage_table'))
    item_id = fields.Char(string=_('archives_class_manage_item_id'))
    item_name = fields.Char(string=_('archives_class_manage_item_name'))
    class_name = fields.Char(string=_('archives_class_manage_class_name'))
    # TODO 这是一个Many2one
    class_type = fields.Char(string=_('archives_class_manage_class_type'))
    # TODO 这是一个Many2one
    parent = fields.Char(string=_('archives_class_manage_parent'))
    form_creator = fields.Char(string=_('archives_class_manage_form_creator'))
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
