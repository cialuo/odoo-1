# -*- coding: utf-8 -*-

from odoo import models, fields, api

class questions(models.Model):
     _name = 'employees_growth.questions'
     _description = 'Questions'

     """
        题库：
            题库名称、编号、多选题、单选题
            判断题、创建人、创建时间、题目总数
     """

     name = fields.Char(string='Name',required=True)

     questions_no = fields.Char(string='Questions no',required=True)

     multiselect_question_count = fields.Integer(string='Multiselect question count',compute="_compute_multiselect_question_count")

     radio_question_count = fields.Integer(string='Radio question count',compute="_compute_radio_question_count")

     judge_question_count = fields.Integer(string='Judge question count',compute="_compute_judge_question_count")

     total_count = fields.Integer(string='Total count',compute="_compute_total_count")

     multiselect_questions = fields.One2many('employees_growth.multiselect_question',
                                            'questions_id', copy=True, string='Multiselect question id')

     radio_questions = fields.One2many('employees_growth.radio_question',
                                            'questions_id', copy=True, string='Radio question id')

     judge_questions = fields.One2many('employees_growth.judge_question',
                                            'questions_id',  copy=True, string='Judge question id')

     @api.depends('multiselect_questions','radio_questions','judge_questions')
     def _compute_total_count(self):
         for order in self:
             order.total_count = len(order.multiselect_questions) + len(order.radio_questions) + len(order.judge_questions)

     @api.depends('radio_questions')
     def _compute_radio_question_count(self):
        self.radio_question_count = len(self.radio_questions)

     @api.depends('multiselect_questions')
     def _compute_multiselect_question_count(self):
        self.multiselect_question_count = len(self.multiselect_questions)

     @api.depends('judge_questions')
     def _compute_judge_question_count(self):
            self.judge_question_count =len(self.judge_questions)

class multiselect_question(models.Model):

    _name = 'employees_growth.multiselect_question'
    _description = 'Model_Multiselect question'
    """
        多选题
    """
    questions_id = fields.Many2one('employees_growth.questions')

    name = fields.Char(string='Question name',required=True)

    option_A = fields.Char(string='Option A',required=True)
    option_B = fields.Char(string='Option B',required=True)
    option_C = fields.Char(string='Option C',required=True)
    option_D = fields.Char(string='Option D',required=True)

    answer = fields.Char(string='Answer',required=True)

class radio_question(models.Model):

    _name = 'employees_growth.radio_question'
    _description = 'Model_Radio question'
    """
        单选题
    """
    questions_id = fields.Many2one('employees_growth.questions')

    name = fields.Char(string='Question name',required=True)

    option_A = fields.Char(string='Option A',required=True)
    option_B = fields.Char(string='Option B',required=True)
    option_C = fields.Char(string='Option C',required=True)
    option_D = fields.Char(string='Option D',required=True)

    answer = fields.Char(string='Answer',required=True)

class judge_question(models.Model):

    _name = 'employees_growth.judge_question'
    _description = 'Model_Judge question'
    """
        判断题
    """
    questions_id = fields.Many2one('employees_growth.questions')

    name = fields.Char(string='Question name',required=True)

    option_A = fields.Char(string='Option A',required=True)
    option_B = fields.Char(string='Option B',required=True)
    option_C = fields.Char(string='Option C',required=True)
    option_D = fields.Char(string='Option D',required=True)

    answer = fields.Char(string='Answer',required=True)



