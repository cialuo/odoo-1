# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools

class training_plan(models.Model):

     _name = 'employees_growth.training_plan'
     _description = 'Training plan'

     """
          培训计划：
               培训周期、状态、创建人、创建时间、审核人
               退回备注、课程详情
     """

     name = fields.Char(string='Name')

     training_cycle = fields.Char(string='Training cycle')

     return_remarks = fields.Char(string='Return remarks')

     auditor = fields.Many2one('hr.employee',string='Auditor')

     state = fields.Selection([('draft','Draft'),('pendingAudit','Pending audit'),
                               ('pendingExecution','Pending execution'),('complete','Complete')],default='draft')




     @api.multi
     def draft_to_pendingAudit(self):
         self.state = 'pendingAudit'

     @api.multi
     def pendingAudit_to_pendingExecution(self):
         self.state = 'pendingExecution'

     @api.multi
     def pendingAudit_to_draft(self):
         self.state = 'draft'

     @api.multi
     def pendingExecution_to_complete(self):
         self.state = 'complete'

     @api.multi
     def pendingExecution_to_pendingAudit(self):
         self.state = 'pendingAudit'







