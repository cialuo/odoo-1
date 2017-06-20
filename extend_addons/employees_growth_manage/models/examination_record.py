# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import random

class examination_record(models.Model):

     _inherit = ['employees_growth.curriculum_schedule']

     """
        培训课程表-考试信息：
            及格线、所用试卷、答题现在时间、允许最大考试次数、考生须知
     """

     display_name = fields.Char(string='Display name',compute='_compute_display_name')

     display_code = fields.Char(string='Display code',compute='_compute_display_code')

     passing_score = fields.Integer(string='Passing score')

     total_score = fields.Integer(string='Aggregate score',related='course_id.test_paper_id.aggregate_score',store=True,readonly=True)

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
               order.display_name = order.course_id.name

     @api.multi
     def _compute_display_code(self):
          """
               设置默认的编码
          :return:
          """
          for order in self:
               if order.train_date:
                    order.display_code = order.train_date.replace('-', '').replace(' ', '')

     @api.onchange('passing_score')
     def _onchanget_passing_score(self):
        """
            及格分数不能大于试卷总分数
        :return:
        """
        if self.passing_score > self.total_score:
            self.passing_score = self.total_score


class examination_students(models.Model):

     _inherit = ['employees_growth.students']

     """
          每个考生的考试情况信息
     """



     display_name = fields.Char(related='curriculum_schedule_id.display_name',string='Display name', store=True,readonly=True)

     examination_datetime = fields.Datetime(related='curriculum_schedule_id.examination_datetime', store=True, readonly=True)

     course_id = fields.Many2one(related='curriculum_schedule_id.course_id',string='Course_id', store=True, readonly=True)

     passing_score = fields.Integer(related='curriculum_schedule_id.passing_score', store=True, readonly=True)

     total_score = fields.Integer(string='Aggregate score', related='curriculum_schedule_id.total_score', store=True,
                                readonly=True)

     test_score = fields.Float(string='Test score', default=0,compute='compute_test_score')

     test_results = fields.Selection([('passingExam','Passing Exam'),('failedExam','Failed Exam')],compute='compute_test_results')

     multiselect_score = fields.Float(default=0)

     radio_score = fields.Float(default=0)

     judge_score = fields.Float(default=0)

     state = fields.Selection([('waitingExam','Waiting Exam'),
                               ('canTest','Can Test'),
                               ('examOver','Exam Over')],default='waitingExam')

     radio_question = fields.One2many('employees_growth.students_radio_question','student_id')

     judge_question = fields.One2many('employees_growth.students_judge_question','student_id')

     multiselect_question = fields.One2many('employees_growth.students_multiselect_question','student_id')

     curriculum_state = fields.Selection(related='curriculum_schedule_id.state', store=True, readonly=True)

     test_paper_id = fields.Many2one('employees_growth.test_paper')

     radio_question_count = fields.Integer(related='test_paper_id.radio_question_count',store=True, readonly=True)

     multiselect_question_count = fields.Integer(related='test_paper_id.multiselect_question_count',
                                                 store=True, readonly=True)

     judge_question_count = fields.Integer(related='test_paper_id.judge_question_count',
                                           store=True, readonly=True)

     radio_question_score = fields.Integer(related='test_paper_id.radio_question_score',
                                           store=True, readonly=True)

     multiselect_question_score = fields.Integer(related='test_paper_id.multiselect_question_score',
                                                 store=True, readonly=True)

     judge_question_score = fields.Integer(related='test_paper_id.judge_question_score',
                                           store=True, readonly=True)

     @api.multi
     def compute_test_score(self):
         for order in self:
             order.test_score = order.multiselect_score + order.radio_score + order.judge_score

     @api.multi
     def compute_test_results(self):
         for order in self:
             if order.state == 'examOver':
                 if order.test_score > order.passing_score or order.test_score == order.passing_score:
                     order.test_results = 'passingExam'
                 else:
                     order.test_results = 'failedExam'

     @api.model
     def get_examination_info(self,id):

          #获取考试数据
          student = self.env['employees_growth.students'].search([('id', '=', id)])
          questions= {}

          questions['display_name'] = student.display_name

          for detail in student.curriculum_schedule_id.course_id.test_paper_id.test_paper_details:

              if detail.question_type =='radio_question':
                questions['radio'] = {'count': detail.question_count, 'score': detail.score, 'questions': student.radio_question.read()}
              elif detail.question_type =='multiselect_question':
                  questions['multiselect'] = {'count': detail.question_count, 'score': detail.score,'questions': student.multiselect_question.read()}
              elif detail.question_type == 'judge_question':
                  questions['judge'] = {'count': detail.question_count, 'score': detail.score,'questions': student.judge_question.read()}

          return questions

     @api.model
     def test_calculation(self,vals):
         """
            分数统计
         :param vals:
         :return:
         """
         student = self.env['employees_growth.students'].search([('id', '=', vals.get('student_id')[0])])
         self.calculate_scores(student,vals)

     def calculate_scores(self,student,vals):
         """
            计算分值
         :return:
         """
         counts = self.filter_count(student,vals)

         for detail in student.curriculum_schedule_id.course_id.test_paper_id.test_paper_details:
             if detail.question_type == 'radio_question':
                 student.radio_score = int(counts.get(detail.question_type)) * detail.score
             elif detail.question_type == 'multiselect_question':
                 student.multiselect_score = int(counts.get(detail.question_type)) * detail.score
             elif detail.question_type == 'judge_question':
                 student.judge_score  = int(counts.get(detail.question_type)) * detail.score

         student.state = 'examOver'


     def filter_count(self,student,vals):
         """
            筛选正确的题目数量
         :return:
         """
         multiselect_count = 0
         radio_count = 0
         judge_count = 0
         return_val = {}

         radio_questions = student.radio_question
         multiselect_questions = student.multiselect_question
         judge_questions = student.judge_question

         for answer in vals.get('radio'):

             if answer.get('value'):

                 for radio in radio_questions:
                     if radio.id == int(answer.get('id')):
                         radio.student_answer = answer.get('value')

                     if radio.answer == answer.get('value') and radio.id == int(answer.get('id')):
                        radio_count+=1
                        break

         for answer in vals.get('multiselect'):

             if answer.get('value'):

                 for multiselect in multiselect_questions:

                     if multiselect.id == int(answer.get('id')):
                         multiselect.student_answer = answer.get('value')

                     if multiselect.answer == answer.get('value') and multiselect.id == int(answer.get('id')):
                        multiselect_count+=1
                        break

         for answer in vals.get('judge'):
             if answer.get('value'):
                 for judge in judge_questions:
                     if judge.id == int(answer.get('id')):
                         judge.student_answer = answer.get('value')

                     if judge.answer == answer.get('value') and judge.id == int(answer.get('id')):
                        judge_count+=1
                        break

         return_val['multiselect_question'] = multiselect_count
         return_val['radio_question'] = radio_count
         return_val['judge_question'] = judge_count

         return return_val

class multiselect_question(models.Model):

    _name = 'employees_growth.students_multiselect_question'
    _description = 'Students_Multiselect question'
    """
        学生的多选题
    """
    student_id = fields.Many2one('employees_growth.students')

    name = fields.Char(string='Question name',required=True)

    option_A = fields.Char(string='Option A',required=True)
    option_B = fields.Char(string='Option B',required=True)
    option_C = fields.Char(string='Option C',required=True)
    option_D = fields.Char(string='Option D',required=True)

    answer = fields.Char(string='Answer',required=True)
    student_answer = fields.Char(string='Student Answer')

class radio_question(models.Model):

    _name = 'employees_growth.students_radio_question'
    _description = 'Students_Radio question'
    """
        学生的单选题
    """
    student_id = fields.Many2one('employees_growth.students')

    name = fields.Char(string='Question name',required=True)

    option_A = fields.Char(string='Option A',required=True)
    option_B = fields.Char(string='Option B',required=True)
    option_C = fields.Char(string='Option C',required=True)
    option_D = fields.Char(string='Option D',required=True)

    answer = fields.Char(string='Answer',required=True)
    student_answer = fields.Char(string='Student Answer')

class judge_question(models.Model):

    _name = 'employees_growth.students_judge_question'
    _description = 'Students_Judge question'
    """
        学生的判断题
    """
    student_id = fields.Many2one('employees_growth.students')

    name = fields.Char(string='Question name',required=True)

    option_A = fields.Char(string='Option A',required=True)
    option_B = fields.Char(string='Option B',required=True)
    option_C = fields.Char(string='Option C',required=True)
    option_D = fields.Char(string='Option D',required=True)

    answer = fields.Char(string='Answer',required=True)
    student_answer = fields.Char(string='Student Answer')