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

class User(models.Model):
    _inherit = 'res.users'

    employee_id = fields.Many2one('hr.employee', compute='_get_employee')
    employee_post = fields.Many2one('employees.post', compute='_get_employee')

    @api.multi
    def _get_employee(self):
        for user in self:
            em = self.env['hr.employee'].search([('user_id', '=', user.id)])
            if em:
                user.employee_id = em
            if em.workpost:
                user.employee_post = em.workpost