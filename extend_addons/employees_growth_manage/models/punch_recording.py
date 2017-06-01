# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class punch_recording(models.Model):

     _name = 'employees_growth.punch_recording'
     _description = 'Punch recording'

     """
        签到记录表：
            课程、上课时间、课程表、地点
     """
     name = fields.Char(string='Name')

     course_id = fields.Many2one('employees_growth.course',string='Course id')

     teacher_id = fields.Many2one('employees_growth.training_teacher',string='Teacher id')

     address = fields.Char(string='Curriculum address')

     start_time = fields.Datetime(string='Start time')

     state = fields.Selection([('start','Start'),('sign','Sign'),
                               ('examination','Examination'),('complete','Complete')],default='start')

     total_student = fields.Integer(string='Total student')

     sign_number = fields.Integer(string='Sign number')

     unsign_number = fields.Integer(string='Unsign number')

     sign_rate = fields.Float(string='Sign rate')

     details = fields.One2many('employees_growth.punch_recording_details','punch_recording_id',string='Punch recording details')

class punch_recording_details(models.Model):

     _name = 'employees_growth.punch_recording_details'
     _description = 'Punch recording details'

     """
          签到详情记录：
               编号、员工、公司、部门、是否签到
     """

     punch_recording_id = fields.Many2one('employees_growth.punch_recording',string='Punch recording id')

     student_id = fields.Many2one('hr.employee',string='Student id')

     company_id = fields.Many2one('',string='Company id')

     department_id = fields.Many2one('',string='Department id')

     is_sign = fields.Boolean(default=False)

