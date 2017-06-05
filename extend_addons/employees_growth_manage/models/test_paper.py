# -*- coding: utf-8 -*-

from odoo import models, fields, api

class test_paper(models.Model):
    _name = 'employees_growth.test_paper'
    _description = 'Test paper'

    """
       考试试卷，用于生成试卷视图
    """

    name = fields.Char(string='Name')

    test_paper_no = fields.Char(string='Test paper no')

    questions_id = fields.Many2one('employees_growth.questions', string='Questions id')

    aggregate_score = fields.Integer(string='Aggregate score')

    passing_grade = fields.Integer(string='Passing grade')

    test_paper_details = fields.One2many('employees_growth.test_paper_detail','test_paper_id',string='test_paper_details')


class test_paper_detail(models.Model):
    _name = 'employees_growth.test_paper_detail'
    _description = 'Test paper detail'

    """
       考试试卷设置，用于生成试卷视图
    """

    test_paper_id = fields.Many2one('employees_growth.test_paper', string='test_paper_id')

    question_type = fields.Selection([('radio_question','Radio question'),
                                      ('multiselect_question','Multiselect question'),
                                      ('judge_question','Judge question')],string='Question type')

    question_count = fields.Integer(string='Question count')

    score = fields.Integer(string='Score')

    total_score = fields.Integer(string='Total score')

    questions_total_score = fields.Integer(string='Questions total score')

