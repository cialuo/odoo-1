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

class Employee(models.Model):
    _inherit = 'hr.employee'

    display_code = fields.Char(string='Display Code', compute='_get_display_code')
    jobnumber = fields.Char(size=6)

    @api.depends('department_id', 'workpost')
    def _get_display_code(self):
        """
        （岗位编码，位数：3）（部门编码，位数：3） （员工工号，位数：6） = 显示编号
        :return: 
        """
        for e in self:
            if e.id != 1:
                post_code = ''
                department_code = ''
                if e.department_id:
                    department_code = (e.department_id.code or '')
                if e.workpost:
                    post_code = (e.workpost.code or '')

                e.display_code = post_code + department_code + e.jobnumber

class Post(models.Model):
    _inherit = 'employees.post'

    code = fields.Char(string='Post Code', size=3)
    posttype = fields.Selection(selection_add=[('manager', 'Manager'), ('security', 'Seccurity')])

class Department(models.Model):
    _inherit = 'hr.department'

    code = fields.Char(string='Department Code', size=3)