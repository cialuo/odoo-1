# -*- coding: utf-8 -*-

from odoo import models, fields, api

class course(models.Model):

     _name = 'employees_growth.course'
     _description = 'Course'

     """
        培训课程：
            课程名、编号、创建人、课程了、类别、创建时间
            讲师、学分、试卷、课程介绍、课件、
            教学目的、教课内容
     """
     name = fields.Char(string='Name')

     course_no = fields.Char(string='Course no')

     course_type = fields.Many2one('employees_growth.course_type',string='Course type')

     training_teacher = fields.Many2many('employees_growth.training_teacher',string='Course training teacher')

     test_paper_id = fields.Many2one('employees_growth.test_paper',string='Test paper id')

     course_credit = fields.Float(string='Course credit')

     creat_date = fields.Datetime(string='Creat date')

     course_founder = fields.Many2one('employees_growth.training_teacher', string='Course founder')

     course_introduce = fields.Text(string='Course introduce')

     course_objective = fields.Char(string='Course objective')

     course_content = fields.Text(string='Course content')

     course_enclosure = fields.Many2many('ir.attachment',string='Course enclosure')

