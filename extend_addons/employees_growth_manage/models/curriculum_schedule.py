# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class curriculum_schedule(models.Model):

     _name = 'employees_growth.curriculum_schedule'
     _description = 'Curriculum schedule'

     """
        培训课程表：
            培训时间、培训地点、讲师、学生
     """
     name = fields.Char(string='Name')

     curriculum_no = fields.Char(string='Curriculum no')

     train_type = fields.Selection([('inside','Inside Train'),('external','External Train')],string='Train type',default='inside')

     course_id = fields.Many2one('employees_growth.course',string='Course id')

     course_type = fields.Many2one(string='Course type',related='course_id.course_type', store=False,readonly=True)

     teacher_id = fields.Many2one('employees_growth.training_teacher',string='Teacher id')

     address = fields.Char(string='Curriculum address')

     start_time = fields.Datetime(string='Start time')

     end_time = fields.Datetime(string='End time')

     state = fields.Selection([('start','Start'),('sign','Sign'),
                               ('examination','Examination'),('complete','Complete')],default='start')


     @api.multi
     def start_to_sign(self):
          self.state = 'sign'

     @api.multi
     def sign_to_examination(self):
          self.state = 'examination'

     @api.multi
     def examination_to_complete(self):
          self.state = 'complete'


