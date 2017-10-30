# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class security_check_table(models.Model):

    _name = 'security_manage.check_table'
    _sql_constraints = [('check_item_detail_name_unique', 'unique (name)', u"检查表名称已存在!")]

    check_table_id = fields.Char(string='security_check_table_id')

    name = fields.Char(string='function_module',required=True)

    remarks = fields.Char(string='remarks')

    check_type = fields.Char(string='check_type')

    # TODO many2one
    responser = fields.Many2one('hr.employee', string='check_responser')

    # TODO many2one
    department_id = fields.Many2one('hr.department', related="responser.department_id", string='department id',readonly=True)

    plan_detail = fields.One2many('security_manage.check_item_detail', 'check_table_item_id', copy=True)

    active = fields.Boolean(string="MyActive", default=True)

    state = fields.Selection([
        ('draft', 'Draft_check_table'),
        ('execute', 'Execute_check_table'),
        ('archive', "Archive_check_table"),
    ], default='draft', string='security_check_table_state')

    @api.multi
    def action_to_draft(self):
        self.state = 'draft'
        self.active = True

    @api.multi
    def action_execute(self):
        self.state = 'execute'

    @api.multi
    def action_archive(self):
        self.state = 'archive'
        self.active = False
    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if ('name' not in default) :
            default['name'] = _("%s (copy)") % self.name
        return super(security_check_table, self).copy(default)  


class security_check_table_item(models.Model):

    _name = 'security_manage.check_item_detail'
    _sql_constraints = [('check_item_detail_item_unique', 'unique (check_table_item_id,item_id)', u"存在相同的检查项!")]

    check_table_item_id = fields.Many2one('security_manage.check_table', ondelete='cascade',required=True)

    item_id = fields.Many2one('security_manage.check_item', ondelete='cascade',required=True)

    check_item_name = fields.Char(related='item_id.check_item_name', readonly=1)

    check_content = fields.Char(related='item_id.check_content', readonly=1)

    check_standards = fields.Char(related='item_id.check_standards', readonly=1)

    state = fields.Selection(related='item_id.state', readonly=1)



