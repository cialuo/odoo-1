# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class punch_recording(models.Model):

     _name = 'employees_growth.time_arrangement'
     _description = 'Time arrangement'

     """
          课程表的课时安排：
               一个课时对应一个签到表
               多个课时，对应一个考试列表
     """
     name = fields.Char(string='Name')

     time_no = fields.Char(string='Time no')

     course_id = fields.Many2one('employees_growth.course',string='Course id')

     teacher_id = fields.Many2one('employees_growth.training_teacher',string='Teacher id')

     address = fields.Char(string='Curriculum address')

     start_time = fields.Datetime(string='Start time')

     end_time = fields.Datetime(string='End time')

     state = fields.Selection([('wait', 'Wait'), ('ingSign', 'Ing Sign'),
                               ('havingClass', 'Having Class'), ('complete', 'Complete')],
                              default='wait')

     total_student = fields.Integer(string='Total student')

     sign_number = fields.Integer(string='Sign number')

     unsign_number = fields.Integer(string='Unsign number')

     sign_rate = fields.Float(string='Sign rate')

     details = fields.One2many('employees_growth.punch_recording_details','punch_recording_id',string='Punch recording details')

     curriculum_schedule_id = fields.Many2one('employees_growth.curriculum_schedule', string='Curriculum schedule id')







class punch_recording_details(models.Model):

     _name = 'employees_growth.punch_recording_details'
     _description = 'Punch recording details'

     """
          签到详情记录：
               编号、员工、公司、部门、是否签到
     """

     punch_recording_id = fields.Many2one('employees_growth.punch_recording',string='Punch recording id')

     student_id = fields.Many2one('hr.employee',string='Student id')

     department_id = fields.Many2one('hr.department', string='Department id')

     is_sign = fields.Boolean(default=False)

