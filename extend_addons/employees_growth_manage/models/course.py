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
     name = fields.Char(string='Name',required=True)

     course_no = fields.Char(string='Course no',required=True)

     course_type = fields.Many2one('employees_growth.course_type',string='Course type',required=True)

     training_teacher = fields.Many2many('employees_growth.training_teacher',string='Course training teacher',required=True)

     test_paper_id = fields.Many2one('employees_growth.test_paper',string='Test paper id',required=True)

     course_credit = fields.Float(string='Course credit')

     course_introduce = fields.Text(string='Course introduce')

     course_objective = fields.Char(string='Course objective')

     course_content = fields.Text(string='Course content')

     course_enclosure = fields.Many2many('ir.attachment',string='Course enclosure')

     #average_number = fields.Float(string='Average Number',compute='',store=True)