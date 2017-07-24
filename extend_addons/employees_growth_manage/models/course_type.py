# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class course_type(models.Model):

     _name = 'employees_growth.course_type'
     _description = 'Course type'
     _sql_constraints = [('course_type_name_unique', 'unique (name)', _(u'类型名称已经存在!')),
                         ('course_type_no_unique', 'unique (type_no)', _(u'类型编号已经存在!'))]

     """
        培训课程类型：
            名称、编号、创建人、说明、创建时间
     """
     name = fields.Char(string='Name',required=True)

     type_no = fields.Char(string='Type no',required=True)

     type_explain = fields.Char(string='Type explain',required=True)


