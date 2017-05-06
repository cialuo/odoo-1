# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class security_check_table(models.Model):
    _name = 'security_manage.check_table'
    name = fields.Char(string=_('check_table'), default=_('check_table'))
    check_table_id = fields.Char(string=_('security_check_table_id'))
    function_module = fields.Char(string=_('function_module'))
    remarks = fields.Char(string=_('remarks'))
    check_type = fields.Char(string=_('check_type'))
    # TODO many2one
    responser = fields.Many2one('hr.employee', string=_('check_responser'))
    # TODO many2one
    parent_company = fields.Many2one('hr.employee', string=_('check_parent_company'))

    plan_detail = fields.Many2many('security_manage.check_item', string=_('plan_detail'))

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
