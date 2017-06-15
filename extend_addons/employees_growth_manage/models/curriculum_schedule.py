# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class curriculum_schedule(models.Model):

     _name = 'employees_growth.curriculum_schedule'
     _description = 'Curriculum schedule'
     _rec_name = 'name'

     """
        培训课程表：
            培训时间、培训地点、讲师、学生
     """
     name = fields.Char(string='Name',required=True)

     curriculum_no = fields.Char(string='Curriculum no')

     train_type = fields.Selection([('inside','Inside Train'),('external','External Train')],
                                   string='Train type',default='inside')

     course_id = fields.Many2one('employees_growth.course',string='Course id',required=True)

     course_type = fields.Many2one(string='Course type',related='course_id.course_type', store=True,readonly=True)

     teacher_id = fields.Many2one('employees_growth.training_teacher',string='Teacher id',required=True)

     address = fields.Char(string='Curriculum address')

     train_date = fields.Date(string='Train date',required=True)

     state = fields.Selection([('start','Start'),('sign','Sign'),
                               ('examination','Examination'),
                               ('complete','Complete')],
                              compute='_compute_state')

     plan_id = fields.Many2one('employees_growth.training_plan',string='Plan id')

     plan_state = fields.Selection(related='plan_id.state', store=True,readonly=True,)

     time_arrangements = fields.One2many('employees_growth.time_arrangement',
                                         'curriculum_schedule_id',string='Time arrangements')

     students = fields.One2many('employees_growth.students','curriculum_schedule_id',string='Students')

     @api.multi
     def _compute_state(self):
          """
               根据每一个课程表课时信息来修改课程表的状态：
                    1、所有课时状态为完成时，课程表表状态为考试
                    2、课程表里某一课时为正在上课时，课程表状态为上课
                    3、课程表默认状态为准备
          :return:
          """
          for order in self:
               havingClassCount = 0
               completeCount = 0
               for time in order.time_arrangements:
                    if time.state == 'havingClass':
                         havingClassCount+=1
                    if time.state == 'complete':
                         completeCount+=1

               if len(order.time_arrangements) == 0:
                    order.state = 'start'
                    continue

               if completeCount == len(order.time_arrangements):
                    order.state = 'examination'
                    continue

               if havingClassCount > 0:
                    order.state = 'sign'
                    continue

               order.state = 'start'


     @api.multi
     def sign_to_examination(self):
          self.state = 'examination'

     @api.multi
     def examination_to_complete(self):
          self.state = 'complete'

     @api.multi
     def write(self, vals):
          """
               判断：
                    修改课程表的课时信息时，修改签到表信息
          :param vals:
          :return:
          """
          res = super(curriculum_schedule, self).write(vals)
          if (vals.has_key('time_arrangements') and len(vals.get('time_arrangements')) > 0) \
                 or (vals.has_key('students') and len(vals.get('students')) > 0):
               self._create_punch_recording(vals)
          return res

     @api.model
     def create(self, vals):
         """
               判断：
                    创建与计划无关的课程表时，新增课时签到表信息
         :param vals:
         :return:
         """
         res = super(curriculum_schedule, self).create(vals)
         if (vals.has_key('time_arrangements') and len(vals.get('time_arrangements')) > 0) \
                 or (vals.has_key('students') and len(vals.get('students')) > 0):
              self._create_punch_recording(vals)
         return res

     def _create_punch_recording(self,vals):
          """
               创建签到记录
          :return:
          """

          if self.id:
               """
                    修改课程表
               """
               id = self.id
          else:
               """
                    新建课程表
               """
               if len(vals.get('time_arrangements')) > 0:
                    id = vals.get('time_arrangements')[0][2].get('curriculum_schedule_id')

          if id :
               # 根据课程表ID获取计划
               schedule = self.env['employees_growth.curriculum_schedule'].search([('id', '=', id)])
               students = schedule.students
               times = schedule.time_arrangements
               print 'students:',len(students)
               print 'times:', len(times)

               for time in times:
                    time.details.unlink()
                    for student in students:
                         detail_vals = {
                              'punch_recording_id':time.id,
                              'student_id':student.student_id.id
                         }
                         self.env['employees_growth.punch_recording_details'].create(detail_vals)



class students(models.Model):

     _name = 'employees_growth.students'
     _description = 'Students'

     """
          参加培训的人员：
               姓名，工号，部门
     """

     curriculum_schedule_id = fields.Many2one('employees_growth.curriculum_schedule',string='Curriculum schedule id')

     student_id = fields.Many2one('hr.employee', string='Student id',required=True)

     jobnumber = fields.Char(string='Jobnumber',related='student_id.jobnumber', store=True, readonly=True)

     department_id = fields.Many2one(related='student_id.department_id', string='Department id',store=True, readonly=True)

     post_id = fields.Many2one(related='student_id.workpost', store=True, readonly=True,string='Post id')

     ways_of_registration = fields.Selection([('companyWays', 'Company Ways'),
                                              ('AutonomousWays', 'Autonomous Ways')],
                                             string='ways_of_registration',default='companyWays')

     is_sign = fields.Boolean(default=False)

