# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import datetime

class WarrantyPlan(models.Model): # 车辆保养计划
    _inherit = 'mail.thread'
    _name = 'warranty_plan'
    name = fields.Char(string='Warranty Plan', required=True, index=True)

    plan_month = fields.Date(default=datetime.datetime.utcnow())

    @api.depends('plan_month')
    def _compute_month(self):
        for plan in self:
            tmp_plan_month = datetime.datetime.strftime(datetime.datetime.strptime(plan.plan_month, '%Y-%m-%d'), '%Y-%m')
            plan.month=tmp_plan_month

    month = fields.Char(compute='_compute_month') # 月度

    company_id = fields.Many2one('hr.department', string='Company', required=True, default=lambda self: self.env.user.company_id)

    made_company_id = fields.Many2one('hr.department', string='Made Company', required=True, default=lambda self: self.env.user.company_id)

    auditor_id = fields.Many2one('hr.employee', string="Auditor Man")
    auditor_time = fields.Datetime(string="Auditor Time")

    approval_id = fields.Many2one('hr.employee', string="Approval Man")
    approval_time = fields.Datetime(string="Approval Time")

    remark = fields.Char()

    state = fields.Selection([
        ('draft', 'draft'), # 草稿
        ('commit', 'commit'), # 已提交
        ('audit', 'audit'), # 已审核
        ('execute', 'execute'), # 执行中
        ('done', 'done'), # 完成
    ], readonly=True, default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'
        for plan_order in self.plan_order_ids:
            plan_order.state = 'draft'

    @api.multi
    def action_commit(self):
        self.state = 'commit'
        for plan_order in self.plan_order_ids:
            if plan_order.state == 'draft':
                plan_order.state = 'commit'


    @api.multi
    def action_audit(self):
        self.state = 'audit'
        self.auditor_id = self.env.uid
        self.auditor_time = datetime.datetime.utcnow()

    @api.multi
    def action_execute(self):
        self.state = 'execute'
        self.approval_id = self.env.uid
        self.approval_time = datetime.datetime.utcnow()
        for plan_order in self.plan_order_ids:
            if plan_order.state == 'commit':
                plan_order.state = 'wait'

    @api.multi
    def action_done(self):
        self.state = 'done'

    plan_order_ids = fields.One2many('warranty_plan_order', 'parent_id', 'sheetIds') # 计划单ids

    @api.depends('plan_order_ids')
    def _compute_task_count(self):
        plan_sheet_count=0 # 任务数
        maintain_sheet_count=0 # 已执行
        for plan in self:
            for plan_sheet in plan.plan_order_ids:
                plan_sheet_count += 1
                if plan_sheet.maintain_sheet_id.id:
                    maintain_sheet_count += 1
            plan.task_count=plan_sheet_count
            plan.executed_count=maintain_sheet_count

    task_count = fields.Integer(default=0, compute='_compute_task_count') # 任务数

    executed_count = fields.Integer(default=0, compute='_compute_task_count') # 已执行

    @api.model
    def create(self, vals):
        result = super(WarrantyPlan, self.with_context(mail_create_nolog=True)).create(vals)
        result.message_post(body=_('%s has been added to the plan!') % (result.name,))
        return result


