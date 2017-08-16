# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools,exceptions,_

class training_plan(models.Model):
     _name = 'employees_growth.training_plan'
     _description = 'Training plan'

     """
          培训计划：
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

     curriculum_schedules = fields.One2many('employees_growth.curriculum_schedule','plan_id',
                                            string='Curriculum schedules')

     plan_return_record_ids = fields.One2many('employees_growth.plan_return_record',
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

         return super(training_plan, self).unlink()

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

class plan_return_record(models.Model):

    """
        计划回退记录
    """

    _name = 'employees_growth.plan_return_record'
    _description = 'Plan return record'

    plan_id = fields.Many2one('employees_growth.training_plan', string="Repair Order",required=True, readonly=True)

    inspect_user_id = fields.Many2one('hr.employee', string="Inspect Name",readonly=True)

    name = fields.Char(string='Repair names', related='plan_id.name')

    return_reason = fields.Text("Return reason")

    inspect_return_time = fields.Datetime("Inspect return time")

    sequence = fields.Integer("Sequence")