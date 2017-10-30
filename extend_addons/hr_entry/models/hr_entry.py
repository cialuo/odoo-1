# -*- coding: utf-8 -*-
##############################################################################
#
#
#    Copyright (C) 2017 xiao (715294035@qq.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.
#
##############################################################################
from odoo import api, fields, models
import time

class Entry(models.Model):
    _name = 'hr.entry'
    _inherits = {'hr.employee': 'employee_id'}

    state = fields.Selection([('draft', 'Draft'), ('process', 'process'), ('done', 'Done')], string='States', default='draft')
    leader_id = fields.Many2one('hr.employee', string='Leader', states={'draft': [('readonly', False)]}, readonly=True, ondelete='restrict')
    employee_id = fields.Many2one('hr.employee', string='employee', states={'draft': [('readonly', False)]}, readonly=True)
    age = fields.Integer(string='Age', states={'draft': [('readonly', False)]}, readonly=True)
    ethnology = fields.Char(string='ethnology', states={'draft': [('readonly', False)]}, readonly=True)
    # entry_date = fields.Date(string='Date Entry', states={'draft': [('readonly', False)]}, readonly=True)
    exit_date = fields.Date(string='Date Exit', states={'draft': [('readonly', False)]}, readonly=True)
    reason = fields.Text(string='Reason', states={'draft': [('readonly', False)]}, readonly=True)
    type = fields.Selection([('entry', 'Entry'), ('exit', 'Exit')], string='Order Type')
    active = fields.Boolean(default=True)

    @api.onchange('birthday')
    def _onchange_age(self):
        if self.birthday:
            self.age = time.localtime().tm_year - time.strptime(self.birthday, "%Y-%m-%d").tm_year

    @api.onchange('employee_id')
    def _onchange_jobnumber(self):
        if self.employee_id:
            # entry = self.env['hr.entry'].search([('employee_id', '=', self.employee_id.id), ('type', '=', 'entry')])
            exit_order = self.env['hr.entry'].search(
                [('employee_id', '=', self.employee_id.id), ('type', '=', self.type)])
            if exit_order:
                raise models.ValidationError(u'员工已存在未处理单据')
            # if entry:
            #     self.entrydate = entry.entrydate

    @api.multi
    def action_process(self):
        """
        提交
        :return: 
        """
        return self.write({'state': 'process'})

    @api.multi
    def action_draft(self):
        """
        退回草稿
        :return: 
        """
        return self.write({'state': 'draft'})

    @api.multi
    def action_done(self):
        """
        审核通过
        入职单通过后，员工为在职
        离职单确认后，归档该员工
        :return: 
        """
        for order in self:
            if order.type == 'exit':
                self.employee_id.write({'active': False})
            if order.type == 'entry':
                self.employee_id.write({'employeestate': 'in_work'})
        return self.write({'state': 'done'})

    @api.multi
    def unlink(self):
        """
        控制单据的删除，只能删除草稿状态的单据
        :return: 
        """
        for order in self:
            if not order.state == 'draft':
                raise models.UserError(u'无法删除非草稿状态的单据')
            order.employee_id.unlink()
        return super(Entry, self).unlink()

class Hr(models.Model):
    _inherit = 'hr.employee'

    @api.onchange('user_id')
    def _onchange_user(self):
        """
        关联用户，不修改员工名称
        :return: 
        """
        self.work_email = self.user_id.email
        self.image = self.user_id.image