# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class security_check_table(models.Model):
    _name = 'security_manage.check_table'
    # name = fields.Char(string=_('check_table'), default=_('check_table'))
    check_table_id = fields.Char(string='security_check_table_id')
    name = fields.Char(string='function_module', readonly=True)
    # function_module = fields.Char(string=_('function_module'))
    remarks = fields.Char(string='remarks')
    check_type = fields.Char(string='check_type')
    # TODO many2one
    responser = fields.Many2one('hr.employee', string='check_responser')
    # TODO many2one
    parent_company = fields.Many2one('hr.employee', string='check_parent_company')

    plan_detail = fields.One2many('security_manage.check_item_detail', 'check_table_item_id')

    state = fields.Selection([
        ('draft', 'Draft_check_table'),
        ('execute', 'Execute_check_table'),
        ('archive', "Archive_check_table"),
    ], default='draft', string='security_check_table_state')

    @api.multi
    def action_to_draft(self):
        self.state = 'draft'

    @api.multi
    def action_execute(self):
        self.state = 'execute'

    @api.multi
    def action_archive(self):
        self.state = 'archive'


class security_check_table_item(models.Model):
    _name = 'security_manage.check_item_detail'
    check_table_item_id = fields.Many2one('security_manage.check_table', ondelete='cascade')
    # name = fields.Char(string=_('check_table'), default=_('check_table'))
    item_id = fields.Many2one('security_manage.check_item', ondelete='cascade')
    check_item_name = fields.Char(related='item_id.check_item_name')
    check_content = fields.Char(related='item_id.check_content')
    check_standards = fields.Char(related='item_id.check_standards')
    state = fields.Selection(related='item_id.state')
