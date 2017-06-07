# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import time,datetime
class punch_recording(models.Model):

     _name = 'employees_growth.time_arrangement'
     _description = 'Time arrangement'

     """
          课程表的课时安排：
               一个课时对应一个签到表
               多个课时，对应一个考试列表
     """
     name = fields.Char(string='Name',compute='_compute_name')

     time_no = fields.Char(string='Time no',compute='_compute_time_no')

     teacher_id = fields.Many2one('employees_growth.training_teacher',string='Teacher id',required=True,)

     address = fields.Char(string='Curriculum address',required=True)

     start_time = fields.Datetime(string='Start time',required=True)

     end_time = fields.Datetime(string='End time',required=True)

     state = fields.Selection([('wait', 'Wait'), ('ingSign', 'Ing Sign'),
                               ('havingClass', 'Having Class'), ('complete', 'Complete')],
                              default='wait')

     total_student = fields.Float(string='Total student',compute='_compute_total_student')

     sign_number = fields.Float(string='Sign number',compute='_compute_sign_number')

     unsign_number = fields.Float(string='Unsign number',compute='_compute_unsign_number')

     sign_rate = fields.Char(string='Sign rate',compute='_compute_sign_rate')

     details = fields.One2many('employees_growth.punch_recording_details','punch_recording_id',
                               string='Punch recording details')

     curriculum_schedule_id = fields.Many2one('employees_growth.curriculum_schedule',
                                              string='Curriculum schedule id')

     course_id = fields.Many2one('employees_growth.course',related='curriculum_schedule_id.course_id',
                                 string='Course id', store=True,
                                 readonly=True)

     @api.multi
     def _compute_name(self):
          """
               设置名称规则：
                    讲师:课程
          :return:
          """
          for order in self:
               order.name = order.teacher_id.name + u'的' + order.course_id.name + u'培训'

     @api.multi
     def _compute_time_no(self):
          """
               设置编号规则:
               上课时间
          :return:
          """
          for order in self:
               order.time_no = order.start_time.replace('-', '').replace(':', '').replace(' ', '')

     @api.multi
     def _compute_total_student(self):
          """
               学员人数
          :return:
          """
          for order in self:
               order.total_student = len(order.details)

     @api.multi
     def _compute_unsign_number(self):
          """
               未签到人数
          :return:
          """
          for order in self:
               domain = ['&',('punch_recording_id', '=', order.id),('is_sign','=',False)]
               order.unsign_number = len(self.env['employees_growth.punch_recording_details'].search(domain))

     @api.multi
     def _compute_sign_number(self):
          """
               签到人数
          :return:
          """
          for order in self:
               domain = ['&',('punch_recording_id','=', order.id),('is_sign', '=',True)]
               order.sign_number = len(self.env['employees_growth.punch_recording_details'].search(domain))

     @api.multi
     def _compute_sign_rate(self):
          """
               签到率
          :return:
          """
          for order in self:
               if order.total_student > 0:
                    order.sign_rate = str(round(order.sign_number / order.total_student,3) * 100) + "%"
               else:
                    order.sign_rate = "0.0%"

     @api.multi
     def to_complete(self):
          """
               全部签到
          :return:
          """
          self.state = 'havingClass'

class punch_recording_details(models.Model):

     _name = 'employees_growth.punch_recording_details'
     _description = 'Punch recording details'

     """
          签到详情记录：
               编号、员工、公司、部门、是否签到
     """

     punch_recording_id = fields.Many2one('employees_growth.punch_recording',string='Punch recording id')

     student_id = fields.Many2one('hr.employee',string='Student id', readonly=True)

     jobnumber = fields.Char(string='Jobnumber', related='student_id.jobnumber', store=True, readonly=True)

     department_id = fields.Many2one(related='student_id.department_id', store=True, readonly=True, string='Department id')

     is_sign = fields.Boolean(default=False)

