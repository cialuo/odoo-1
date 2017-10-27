# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime,time
from dateutil.relativedelta import relativedelta
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

     average_score = fields.Float(string='Average Score',store=True,compute='_compute_average_score')

     student_ids = fields.One2many('employees_growth.students','course_id',string='studentids')

     def _compute_average_score(self):
          """
               计算当月平均分
          :return:
          """

          for order in self:
               if order.student_ids:
                    today = datetime.datetime.now()
                    begin_month = today.strftime('%Y-%m-01 00:00:00')
                    end_month = (today + relativedelta(months=1, day=1, days=-1)).strftime('%Y-%m-%d 23:59:59')
                    order.average_score = sum(order.student_ids.filtered(
                         lambda r: r.examination_datetime >= begin_month and r.examination_datetime <= end_month).mapped('total_score'))
               else:
                    order.average_score = 0.0

