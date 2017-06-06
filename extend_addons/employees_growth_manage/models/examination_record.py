# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class examination_record(models.Model):

     _inherit = ['employees_growth.curriculum_schedule']

     """
        培训课程表-考试信息：
            及格线、所用试卷、答题现在时间、允许最大考试次数、考生须知
     """

     passing_score = fields.Float(string='Passing score')

     time_limit = fields.Integer(string='Time limit')

     frequency = fields.Integer(string='Frequency')

     tips_for_candidates = fields.Text(string='Tips for candidates')






