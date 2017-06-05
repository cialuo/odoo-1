# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class examination_record(models.Model):

     _inherit = ['employees_growth.curriculum_schedule']

     """
        培训课程表-考试信息：
            及格线、所用试卷、答题现在时间、允许最大考试次数、考生须知
     """

     examiners_details = fields.One2many('employees_growth.examiners_details',
                                         'curriculum_schedule_id',string='Examiners details')

     passing_score = fields.Float(string='Passing score')

     time_limit = fields.Integer(string='Time limit')

     frequency = fields.Integer(string='Frequency')

     tips_for_candidates = fields.Text(string='Tips for candidates')


class examiners_details(models.Model):

    _name = 'employees_growth.examiners_details'
    _description = 'Examiners details'

    """
        参考人员：
            数据基于表数据
    """

    curriculum_schedule_id = fields.Many2one('employees_growth.curriculum_schedule',string='Curriculum schedule id')

    student_id = fields.Many2one('hr.employee', string='Student id')

    department_id = fields.Many2one('hr.department', string='Department id')

    ways_of_registration = fields.Selection([('companyWays','Company Ways'),
                                             ('AutonomousWays','Autonomous Ways')],string='ways_of_registration')





