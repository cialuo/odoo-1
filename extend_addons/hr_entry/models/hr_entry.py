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

class Entry(models.Model):
    _name = 'hr.entry'
    _inherits = {'hr.employee': 'employee_id'}

    state = fields.Selection([('draft', 'Draft'), ('process', 'process'), ('done', 'Done')], string='States', default='draft')
    leader_id = fields.Many2one('hr.employee', string='Leader')
    employee_id = fields.Many2one('hr.employee', string='employee')
    age = fields.Integer(string='Age')
    ethnology = fields.Char(string='ethnology')
    entry_date = fields.Date(string='Date Entry')
    exit_date = fields.Date(string='Date Exit')
    reason = fields.Text(string='Reason')
    type = fields.Selection([('entry', 'Entry'), ('exit', 'Exit')], string='Order Type')
    active = fields.Boolean(default=True)

    @api.onchange('employee_id')
    def _onchange_jobnumber(self):
        if self.employee_id:
            entry = self.env['hr.entry'].search([('employee_id', '=', self.employee_id.id), ('type', '=', 'entry')])
            if entry:
                self.entry_date = entry.entry_date
            exit_order = self.env['hr.entry'].search(
                [('employee_id', '=', self.employee_id.id), ('type', '=', self.type)])
            if exit_order:
                raise models.ValidationError(u'员工已存在未处理单据')

    @api.multi
    def action_process(self):
        return self.write({'state': 'process'})

    @api.multi
    def action_draft(self):
        return self.write({'state': 'draft'})

    @api.multi
    def action_done(self):
        for order in self:
            if order.type == 'exit':
                self.employee_id.write({'active': False})
        return self.write({'state': 'done'})