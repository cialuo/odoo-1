# -*- coding: utf-8 -*-

from odoo import models, fields, api,_,exceptions

class test_paper(models.Model):
    _name = 'employees_growth.test_paper'
    _description = 'Test paper'

    """
       考试试卷，用于生成试卷视图
    """

    name = fields.Char(string='Name',required=True)

    test_paper_no = fields.Char(string='Test paper no',required=True)

    questions_id = fields.Many2one('employees_growth.questions', string='Questions id',required=True)

    aggregate_score = fields.Integer(string='Aggregate score',compute="_compute_aggregate_score")

    passing_grade = fields.Integer(string='Passing grade')

    test_paper_details = fields.One2many('employees_growth.test_paper_detail','test_paper_id',string='test_paper_details')

    @api.multi
    def _compute_aggregate_score(self):
        """
            计算试卷总分数：
                题型数 * 题型总分
        :return:
        """
        for test_paper in self:
            details = self.env['employees_growth.test_paper_detail'].search([('test_paper_id', '=', test_paper.id)])
            if len(details) > 0:
                test_paper.aggregate_score = sum(details.mapped('total_score'))

class test_paper_detail(models.Model):
    _name = 'employees_growth.test_paper_detail'
    _description = 'Test paper detail'
    _sql_constraints = [('question_type_unique', 'unique(question_type,test_paper_id)', u'存在相同题型!')]

    """
       考试试卷设置，用于生成试卷视图
    """

    test_paper_id = fields.Many2one('employees_growth.test_paper', string='test_paper_id')

    question_type = fields.Selection([('radio_question','Radio question'),
                                      ('multiselect_question','Multiselect question'),
                                      ('judge_question','Judge question')],string='Question type',required=True)

    question_count = fields.Integer(string='Question count',required=True)

    score = fields.Integer(string='Score',required=True)

    total_score = fields.Integer(string='Total score',compute='_compute_total_score')

    @api.depends('question_count','score')
    def _compute_total_score(self):
        """
            计算题型合计：
                题数 * 单题分值
        :return:
        """
        for detail in self:
            detail.total_score = detail.question_count * detail.score

    @api.onchange('question_count')
    def _onchanget_question_count(self):
        """
            判断输入数量和题库中数量
        :return:
        """
        if self.question_type == 'radio_question':
            if self.test_paper_id.questions_id.radio_question_count < self.question_count:
                self.question_count = self.test_paper_id.questions_id.radio_question_count

        elif self.question_type == 'multiselect_question':
            if self.test_paper_id.questions_id.multiselect_question_count < self.question_count:
                self.question_count = self.test_paper_id.questions_id.multiselect_question_count

        elif self.question_type == 'judge_question':
            if self.test_paper_id.questions_id.judge_question_count < self.question_count:
                self.question_count = self.test_paper_id.questions_id.judge_question_count