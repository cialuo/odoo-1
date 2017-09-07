# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools,exceptions,_

class external_training_plan(models.Model):

     _name = 'employees_growth.external_training_plan'
     _description = 'External training plan'

     """
          外部培训计划：
               培训周期、状态、创建人、创建时间、审核人
               退回备注、课程详情
     """

     name = fields.Char(string='Name',required=True)

     training_cycle = fields.Char(string='Training cycle')

     return_remarks = fields.Char(string='Return remarks',readonly=True)

     auditor = fields.Many2one('hr.employee',string='Auditor')

     auditor_time = fields.Datetime(string='Auditor time')

     state = fields.Selection([('draft','Draft'),('pendingAudit','Pending audit'),
                               ('pendingExecution','Pending execution'),
                               ('complete','Complete')],default='draft')

     curriculum_schedules = fields.One2many('employees_growth.external_curriculum_schedule','plan_id',copy=True,
                                            string='Curriculum schedules')

     plan_return_record_ids = fields.One2many('employees_growth.external_plan_return_record',
                                              'plan_id',
                                              string='Plan return record ids')

     @api.multi
     def unlink(self):
         """
         控制单据的删除，只能删除草稿状态的单据
         :return:
         """
         for order in self:
             if not order.state == 'draft':
                 raise exceptions.UserError(_('Only the plan to delete the draft status.'))

         return super(external_training_plan, self).unlink()

     def _default_employee(self):
         """
            获取前员工
         :return:
         """
         emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
         return emp_ids and emp_ids[0] or False

     @api.multi
     def draft_to_pendingAudit(self):
         self.state = 'pendingAudit'

     @api.multi
     def pendingAudit_to_pendingExecution(self):
         emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
         if emp_ids :
             self.auditor = emp_ids[0].id
             self.state = 'pendingExecution'
         else :
            raise exceptions.UserError(_("Please relation user to employee first!"))

     @api.multi
     def pendingAudit_to_draft(self,reason=''):
         """
            退回重做：
                1、记录每一次退回重做保存到数据库
                2、显示最后一条退回记录
                3、修改单据状态
         :param reason:
         :return:
         """
         inspect_return_time = fields.Datetime.now()

         inspect_user_id = self._default_employee().id if self._default_employee() else ''

         vals = {
             "repair_id": self.id,
             "inspect_return_time": inspect_return_time,
             "return_reason": reason,
             "inspect_user_id": inspect_user_id,
             "sequence": len(self.plan_return_record_ids) + 1
         }
         self.write({
             "state": 'draft',
             "auditor_time": inspect_return_time,
             "auditor": inspect_user_id,
             "plan_return_record_ids": [(0, 0, vals)],
             "return_remarks":reason
         })

     @api.multi
     def pendingExecution_to_complete(self):
         self.state = 'complete'

     @api.multi
     def pendingExecution_to_pendingAudit(self):
         self.state = 'pendingAudit'

class external_plan_return_record(models.Model):

    """
        计划回退记录
    """

    _name = 'employees_growth.external_plan_return_record'
    _description = 'External plan return record'

    plan_id = fields.Many2one('employees_growth.external_training_plan', string="Repair Order",required=True, readonly=True)

    inspect_user_id = fields.Many2one('hr.employee', string="Inspect Name",readonly=True)

    name = fields.Char(string='Repair names', related='plan_id.name')

    return_reason = fields.Text("Return reason")

    inspect_return_time = fields.Datetime("Inspect return time")

    sequence = fields.Integer("Sequence")


class external_curriculum_schedule(models.Model):
    _name = 'employees_growth.external_curriculum_schedule'
    _description = 'External curriculum schedule'
    _rec_name = 'course_id'
    """
       培训课程表：
           培训时间、培训地点、讲师、学生
    """

    plan_id = fields.Many2one('employees_growth.external_training_plan', string='Plan id')

    plan_state = fields.Selection(related='plan_id.state', store=True,readonly=True)

    name = fields.Char(string='Name', related='plan_id.name', store=True, readonly=True)

    training_cycle = fields.Char(related='plan_id.training_cycle', store=True, readonly=True,string='Training cycle')

    train_type = fields.Selection([('inside', 'Inside Train'), ('external', 'External Train')],
                                  string='Train type', default='external',readonly=True)

    course_id = fields.Many2one('employees_growth.course', string='Course id', required=True)

    course_type = fields.Many2one(string='Course type', related='course_id.course_type', store=False, readonly=True)

    teacher_id = fields.Many2one('employees_growth.training_teacher',
                                 string='Teacher id', required=True,
                                 domain=[('teacher_type','=','external')])

    address = fields.Char(string='Curriculum address')

    training_institutions = fields.Char(string='Training institutions')

    train_date = fields.Datetime(string='Train date', required=True)

    state = fields.Selection([('draft', 'Draft'), ('pendingExecution', 'Pending execution'),
                              ('execution', 'Execution'),
                              ('complete', 'Complete')],
                             default='draft')

    students = fields.One2many('employees_growth.external_students', 'curriculum_schedule_id', string='Students',copy=True)

    @api.multi
    def start_to_sign(self):
        self.state = 'pendingExecution'

    @api.multi
    def sign_to_examination(self):
        self.state = 'execution'

    @api.multi
    def examination_to_complete(self):
        self.state = 'complete'


class external_students(models.Model):
    _name = 'employees_growth.external_students'
    _description = 'External students'

    _sql_constraints = [
        ('check_external_students_unique',
         'unique(curriculum_schedule_id,student_id)',
         u'存在相同的培训人员!')
    ]

    """
         参加培训的人员：
              姓名，工号，部门
    """

    curriculum_schedule_id = fields.Many2one('employees_growth.external_curriculum_schedule', string='Curriculum schedule id',ondelete='cascade')

    student_id = fields.Many2one('hr.employee', string='Student id', required=True)

    jobnumber = fields.Char(string='Jobnumber', related='student_id.jobnumber', store=True, readonly=True)

    department_id = fields.Many2one(related='student_id.department_id', string='Department id', store=True,
                                    readonly=True)

    post_id = fields.Many2one(related='student_id.workpost', store=True, readonly=True, string='Post id')

    ways_of_registration = fields.Selection([('companyWays', 'Company Ways'),
                                             ('AutonomousWays', 'Autonomous Ways')],
                                            string='ways_of_registration', default='companyWays')

    is_sign = fields.Boolean(default=False)
