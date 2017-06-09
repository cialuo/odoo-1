# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class examination_record(models.Model):

     _inherit = ['employees_growth.curriculum_schedule']

     """
        培训课程表-考试信息：
            及格线、所用试卷、答题现在时间、允许最大考试次数、考生须知
     """

     display_name = fields.Char(string='Display name',compute='_compute_display_name')

     display_code = fields.Char(string='Display code',compute='_compute_display_code')

     passing_score = fields.Float(string='Passing score')

     time_limit = fields.Integer(string='Time limit',default='60')

     frequency = fields.Integer(string='Frequency',default='1')

     tips_for_candidates = fields.Text(string='Tips for candidates')

     test_paper_id = fields.Many2one(string='Test paper id',related='course_id.test_paper_id',store=True,readonly=True)

     examination_datetime = fields.Datetime()

     @api.multi
     def _compute_display_name(self):
          """
               设置默认的名字
          :return:
          """
          for order in self:
               order.display_name = order.course_id.name + u"考试"

     @api.multi
     def _compute_display_code(self):
          """
               设置默认的编码
          :return:
          """
          for order in self:
               if order.train_date:
                    order.display_code = order.train_date.replace('-', '').replace(' ', '')




class examination_students(models.Model):

     _inherit = ['employees_growth.students']

     """
          每个考生的考试情况信息
     """



     display_name = fields.Char(related='curriculum_schedule_id.display_name',string='Display name', store=True,readonly=True)

     examination_datetime = fields.Datetime(related='curriculum_schedule_id.examination_datetime', store=True, readonly=True)

     course_id = fields.Many2one(related='curriculum_schedule_id.course_id',string='Course_id', store=True, readonly=True)

     passing_score = fields.Float(related='curriculum_schedule_id.passing_score', store=True, readonly=True)

     test_score = fields.Float(string='Test score', default=0)

     test_results = fields.Selection([('passingExam','Passing Exam'),('failedExam','Failed Exam')])

     multiselect__score = fields.Float(default=0)

     radio__score = fields.Float(default=0)

     judge__score = fields.Float(default=0)

     state = fields.Selection([('waitingExam','Waiting Exam'),
                               ('canTest','Can Test'),
                               ('examOver','Exam Over')],default='waitingExam')