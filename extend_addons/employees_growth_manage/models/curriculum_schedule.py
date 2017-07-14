# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import random
import datetime

class curriculum_schedule(models.Model):

     _name = 'employees_growth.curriculum_schedule'
     _description = 'Curriculum schedule'
     _rec_name = 'name'

     """
        培训课程表：
            培训时间、培训地点、讲师、学生
     """
     name = fields.Char(string='Name',required=True)

     curriculum_no = fields.Char(string='Curriculum no',default='/',readonly=True)

     train_type = fields.Selection([('inside','Inside Train'),('external','External Train')],
                                   string='Train type',default='inside')

     course_id = fields.Many2one('employees_growth.course',string='Course id',required=True)

     course_type = fields.Many2one(string='Course type',related='course_id.course_type', store=True,readonly=True)

     teacher_id = fields.Many2one('employees_growth.training_teacher',string='Teacher id',required=True,domain=[('teacher_type','=','inside')])

     address = fields.Char(string='Curriculum address')

     train_date = fields.Date(string='Train date',required=True)

     state = fields.Selection([('start','Start'),('sign','Sign'),
                               ('examination','Examination'),
                               ('complete','Complete')],
                              default='start')

     plan_id = fields.Many2one('employees_growth.training_plan',string='Plan id')

     plan_state = fields.Selection(related='plan_id.state', store=True,readonly=True,)

     time_arrangements = fields.One2many('employees_growth.time_arrangement',
                                         'curriculum_schedule_id',string='Time arrangements')

     students = fields.One2many('employees_growth.students','curriculum_schedule_id',string='Students')


     def get_curriculum_no(self,vals):
          """
               选择课程时修改编号的值：
                    所选课程的编码+年月日+01补位
          :return:
          """
          curriculum_no = "/"
          course = self.env['employees_growth.course'].search([('id','=',vals.get('course_id'))])

          start_date =  fields.datetime.utcnow().strftime('%Y-%m-%d 00:00:00')
          end_date = fields.datetime.utcnow().strftime('%Y-%m-%d 23:59:59')
          domain = [('course_id','=',vals.get('course_id')),('create_date','>=',start_date),('create_date','<=',end_date)]
          schedule = self.env['employees_growth.curriculum_schedule'].search(domain,limit=1, order="create_date desc")
          if schedule:
               if schedule.curriculum_no:
                    index = schedule.curriculum_no[len(schedule.curriculum_no)-1:]
                    if len(index) > 0 :

                         index = int(index) + 1

                         if len(str(index)) == 1:
                              index = "0" + str(index)

                         curriculum_no = course.course_no + fields.datetime.utcnow().strftime('%Y%m%d') + index
                    else:
                         curriculum_no = course.course_no + fields.datetime.utcnow().strftime('%Y%m%d') + "01"
          else:
               curriculum_no = course.course_no + fields.datetime.utcnow().strftime('%Y%m%d') + "01"

          return curriculum_no
     @api.multi
     def sign_to_examination(self):
          self.state = 'examination'

          self.save_student_questions()


     def save_student_questions(self):
          """
               保存当前课程表里的所有培训学员的考试题目
          :return:
          """
          for student in self.students:
               student.test_paper_id = self.course_id.test_paper_id
               self.get_questions(student)

     def save_radio_question(self,id,questions,type):
          """
               保存
          :return:
          """
          for question in questions:

               vals = {
                    "student_id":id,
                    "name":question.name,
                    "option_A":question.option_A,
                    "option_B":question.option_B,
                    "option_C":question.option_C,
                    "option_D":question.option_D,
                    "answer":question.answer
               }
               if type == 'radio_question':
                    self.env['employees_growth.students_radio_question'].create(vals)
               elif type == 'multiselect_question':
                    self.env['employees_growth.students_multiselect_question'].create(vals)
               elif type =='judge_question':
                    self.env['employees_growth.students_judge_question'].create(vals)

     def get_questions(self,student):
          """
               获取题目
          :return:
          """
          #试卷详情
          details = student.curriculum_schedule_id.course_id.test_paper_id.test_paper_details
          #题库
          questions_id = student.curriculum_schedule_id.course_id.test_paper_id.questions_id

          for detail in details:

               if detail.question_type == 'radio_question':
                    # 单选题
                    self.save_radio_question(student.id, self.get_random_question(questions_id.radio_questions,
                                                                                  detail.question_count),detail.question_type)
               elif detail.question_type == 'multiselect_question':
                    # 多选题
                    self.save_radio_question(student.id, self.get_random_question(questions_id.multiselect_questions,
                                                                                  detail.question_count),detail.question_type)
               elif detail.question_type == 'judge_question':
                    # 判断题
                    self.save_radio_question(student.id, self.get_random_question(questions_id.judge_questions,
                                                                                  detail.question_count),detail.question_type)


     def get_random_question(self,questions,count):
            """
                遍历各个题库去值
            """
            array = []
            indexArray = []
            while len(array) < count:
                index = random.randint(0, len(questions)-1)
                if indexArray.count(index) > 0:
                    continue
                    indexArray.append(index)
                array.append(questions[index])

            return array

     @api.multi
     def examination_to_complete(self):
          """
               所有的课程完成时，修改培训计划的状态,修改所以课时状态为完成
          :return:
          """
          self.state = 'complete'

          if self.plan_id:
              if self.plan_id.curriculum_schedules.mapped('state').count('complete') == len(self.plan_id.curriculum_schedules):
                    self.plan_id.state = 'complete'

          for time in self.time_arrangements:
               time.state = 'complete'

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

         vals['curriculum_no'] = self.get_curriculum_no(vals)

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
     _sql_constraints = [('check_students_unique', 'unique (curriculum_schedule_id,student_id)', u"存在相同的培训人员!")]
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

