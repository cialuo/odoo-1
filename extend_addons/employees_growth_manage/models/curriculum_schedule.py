# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class curriculum_schedule(models.Model):

     _name = 'employees_growth.curriculum_schedule'
     _description = 'Curriculum schedule'

     """
        培训课程表：
            培训时间、培训地点、讲师、学生
     """
     name = fields.Char(string='Name',required=True)

     curriculum_no = fields.Char(string='Curriculum no')

     train_type = fields.Selection([('inside','Inside Train'),('external','External Train')],
                                   string='Train type',default='inside')

     course_id = fields.Many2one('employees_growth.course',string='Course id',required=True)

     course_type = fields.Many2one(string='Course type',related='course_id.course_type', store=False,readonly=True)

     teacher_id = fields.Many2one('employees_growth.training_teacher',string='Teacher id',required=True)

     address = fields.Char(string='Curriculum address')

     train_date = fields.Date(string='Train date')

     state = fields.Selection([('start','Start'),('sign','Sign'),
                               ('examination','Examination'),
                               ('complete','Complete')],
                              default='start')

     plan_id = fields.Many2one('employees_growth.training_plan',string='Plan id')

     time_arrangements = fields.One2many('employees_growth.time_arrangement',
                                         'curriculum_schedule_id',string='Time arrangements')

     students = fields.One2many('employees_growth.students','curriculum_schedule_id',string='Students')

     @api.multi
     def start_to_sign(self):
          self.state = 'sign'

     @api.multi
     def sign_to_examination(self):
          self.state = 'examination'

     @api.multi
     def examination_to_complete(self):
          self.state = 'complete'


class students(models.Model):

     _name = 'employees_growth.students'
     _description = 'Students'

     """
          参加培训的人员：
               姓名，工号，部门
     """

     curriculum_schedule_id = fields.Many2one('employees_growth.curriculum_schedule',string='Curriculum schedule id')

     student_id = fields.Many2one('hr.employee', string='Student id')

     department_id = fields.Many2one('hr.department', string='Department id')

