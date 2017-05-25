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

     name = fields.Char(string='Name')

     questions_no = fields.Char(string='Questions no')

     multiselect_question_count = fields.Integer(string='Multiselect question count',compute="_compute_multiselect_question_count")

     radio_question_count = fields.Integer(string='Radio question count',compute="_compute_radio_question_count")

     judge_question_count = fields.Integer(string='Judge question count',compute="_compute_judge_question_count")

     total_count = fields.Integer(string='Total count',compute="_compute_total_count")

     questions_founder = fields.Many2one('employees_growth.training_teacher',string='Questions founder')

     multiselect_questions = fields.One2many('employees_growth.multiselect_question',
                                            'questions_id',string='Multiselect question id')

     radio_questions = fields.One2many('employees_growth.radio_question',
                                            'questions_id', string='Radio question id')

     judge_questions = fields.One2many('employees_growth.judge_question',
                                            'questions_id', string='Judge question id')

     @api.depends('multiselect_questions','radio_questions','judge_questions')
     def _compute_total_count(self):
         self.total_count = len(self.multiselect_questions) + len(self.radio_questions) + len(self.judge_questions)

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

    name = fields.Char(string='Question name')

    option_A = fields.Char(string='Option A')
    option_B = fields.Char(string='Option B')
    option_C = fields.Char(string='Option C')
    option_D = fields.Char(string='Option D')

    answer = fields.Char(string='Answer')

class radio_question(models.Model):

    _name = 'employees_growth.radio_question'
    _description = 'Model_Radio question'
    """
        单选题
    """
    questions_id = fields.Many2one('employees_growth.questions')

    name = fields.Char(string='Question name')

    option_A = fields.Char(string='Option A')
    option_B = fields.Char(string='Option B')
    option_C = fields.Char(string='Option C')
    option_D = fields.Char(string='Option D')

    answer = fields.Char(string='Answer')

class judge_question(models.Model):

    _name = 'employees_growth.judge_question'
    _description = 'Model_Judge question'
    """
        判断题
    """
    questions_id = fields.Many2one('employees_growth.questions')

    name = fields.Char(string='Question name')

    option_A = fields.Char(string='Option A')
    option_B = fields.Char(string='Option B')
    option_C = fields.Char(string='Option C')
    option_D = fields.Char(string='Option D')

    answer = fields.Char(string='Answer')



