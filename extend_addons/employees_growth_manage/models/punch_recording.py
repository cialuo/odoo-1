# -*- coding: utf-8 -*-

from odoo import models, fields, api,_,exceptions
import random
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

     @api.constrains('start_time','end_time')
     def check_datetime(self):
          """
               检查课时的开始时间和结束时间
          :return:
          """
          for order in self:
              if order.start_time > order.end_time:
                   raise exceptions.ValidationError(_("Start can not be greater than the end time"))


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
     def ingSign_to_havingClass(self):
          """
               全部签到
          :return:
          """
          self.state = 'havingClass'
          self.curriculum_schedule_id.state = 'sign'

     @api.multi
     def to_complete(self):
          """
               判断是否为当前课程表的最后一个课时,是的话修改课程表状态为：考试
               并且为每一个培训人员生成考题
          :return:
          """
          self.state = 'complete'

          if self.curriculum_schedule_id.time_arrangements.mapped('state').count('complete') == len(self.curriculum_schedule_id.time_arrangements):

               self.curriculum_schedule_id.state = 'examination'

               self.save_student_questions()

     def save_student_questions(self):
          """
               保存当前课程表里的所有培训学员的考试题目
          :return:
          """
          for student in self.curriculum_schedule_id.students:
               student.test_paper_id = self.curriculum_schedule_id.course_id.test_paper_id
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
                遍历各个题库取值
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

class punch_recording_details(models.Model):

     _name = 'employees_growth.punch_recording_details'
     _description = 'Punch recording details'

     """
          签到详情记录：
               编号、员工、公司、部门、是否签到
     """

     punch_recording_id = fields.Many2one('employees_growth.time_arrangement',string='Punch recording id')

     student_id = fields.Many2one('hr.employee',string='Student id', readonly=True)

     jobnumber = fields.Char(string='Jobnumber', related='student_id.jobnumber', store=True, readonly=True)

     department_id = fields.Many2one(related='student_id.department_id', store=True, readonly=True, string='Department id')

     is_sign = fields.Boolean(default=False)

     @api.multi
     def write(self, vals):
          """
               修改签到详情时判断是否签到完成
          :param vals:
          :return:
          """

          res = super(punch_recording_details, self).write(vals)

          if vals.has_key('is_sign'):
               if self.punch_recording_id.details.mapped('is_sign').count(True) > 0:
                    self.punch_recording_id.state = 'ingSign'
               if self.punch_recording_id.details.mapped('is_sign').count(True) == len(self.punch_recording_id.details):
                    self.punch_recording_id.state = 'havingClass'
                    self.punch_recording_id.curriculum_schedule_id.state = 'sign'
          return res
