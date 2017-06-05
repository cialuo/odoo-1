# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class course_type(models.Model):

     _name = 'employees_growth.course_type'
     _description = 'Course type'
     _sql_constraints = [('course_type_name_unique', 'unique (name)', _('The name already exists.')),
                         ('course_type_no_unique', 'unique (type_no)', _('Number already exists.'))]

     """
        培训课程类型：
            名称、编号、创建人、说明、创建时间
     """
     name = fields.Char(string='Name')

     type_no = fields.Char(string='Type no')

     type_explain = fields.Char(string='Type explain')


