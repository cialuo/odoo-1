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

     @api.model
     def get_examination_info(self,id):

          #获取考试数据
          student = self.env['employees_growth.students'].search([('id', '=', id)])
          questions = student.curriculum_schedule_id.course_id.test_paper_id
          r_questions = self.get_questions(questions)
          print r_questions
          return r_questions

     def get_questions(self,test_paper):
         """
            根据试卷信息获取题目列表
         :return:
         """
         questions = {}
         for detail in test_paper.test_paper_details:
            if detail.question_type == 'radio_question':
                #题目数量
                radio_count = detail.question_count
                #题目分值
                radio_score = detail.score
                #总的题目
                radio_questions = test_paper.questions_id.radio_questions
                #随机的题目
                question = self.get_question(radio_questions,radio_count)
                radio = {'radio_count':radio_count,'radio_score':radio_score,'radio_questions':question}
                questions['radio'] =radio

                 #elif detail.question_type == 'multiselect_question':
                     #multiselect_count = detail.question_count
                 #elif detail.question_type == 'judge_question':
                     #judge_count = detail.question_count
         return questions

     def get_question(self,questions,count):
            """
                遍历各个题库去值
            """
            array = []
            indexArray = []
            while len(array) < count:
                index = random.randint(0, len(questions)-1)
                if indexArray.count(index) > 0:
                    continue
                    indexArray.append(index)
                array.append(questions[index])

            return array


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
    student_answer = fields.Char(string='Student Answer',required=True)

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
    student_answer = fields.Char(string='Student Answer', required=True)

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
    student_answer = fields.Char(string='Student Answer', required=True)