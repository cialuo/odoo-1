# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import datetime

class WarrantyPlan(models.Model): # 车辆保养计划
    _inherit = 'mail.thread'
    _name = 'fleet_warranty_plan'
    # name = fields.Char()


    name = fields.Char(string='Plan Number', required=True, index=True) # , default='New' readonly=True, default=lambda self: 'New' required=True, states={'draft': [('readonly', False)]}, index=True,  copy=False,  self: _('New')

    # @api.depends('name')
    # def _compute_tmp_name(self):
    #     for plan in self:
    #         plan.tmp_name=plan.name
    #
    # tmp_name = fields.Char(compute='_compute_tmp_name') # 月度

    # month = fields.Selection(
    #     [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'),
    #      (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=12,
    #     required=True) # 月度

    plan_month = fields.Date(default=datetime.datetime.utcnow())  # string='Order Date', required=True, readonly=True, index=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,default=fields.Datetime.now

    @api.depends('plan_month')
    def _compute_month(self):
        for plan in self:
            tmp_plan_month = datetime.datetime.strftime(datetime.datetime.strptime(plan.plan_month, '%Y-%m-%d'), '%Y-%m')
            plan.month=tmp_plan_month

    month = fields.Char(compute='_compute_month') # 月度

    company_id = fields.Many2one('hr.department', string='Company Id', required=True, default=lambda self: self.env.user.company_id) # company_id = fields.Many2one('res.company', string='Company Id', required=True, default=lambda self: self.env.user.company_id)

    made_company_id = fields.Many2one('hr.department', string='Made Company Id', required=True, default=lambda self: self.env.user.company_id)

    auditor_id = fields.Many2one('hr.employee', string="Auditor Id")
    auditor_time = fields.Datetime(string="Auditor Time")

    approval_id = fields.Many2one('hr.employee', string="Approval Id")
    approval_time = fields.Datetime(string="Approval Time")

    remark = fields.Char()

    state = fields.Selection([
        ('draft', 'draft'), # 草稿
        ('commit', 'commit'), # 已提交
        ('audit', 'audit'), # 已审核
        ('execute', 'execute'), # 执行中
        ('done', 'done'), # 完成
    ], readonly=True, default='draft') # copy=False, index=True, track_visibility='onchange',

    @api.multi
    def action_draft(self):
        self.state = 'draft'
        for item in self.plan_sheet_ids:
            item.state = 'draft'

    @api.multi
    def action_commit(self):
        self.state = 'commit'
        for item in self.plan_sheet_ids:
            if item.state == 'draft':
                item.state = 'commit'

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
        for item in self.plan_sheet_ids:
            if item.state == 'commit':
                item.state = 'wait'

    @api.multi
    def action_done(self):
        self.state = 'done'

    plan_sheet_ids = fields.One2many('fleet_warranty_plan_sheet', 'parent_id', 'sheetIds') # 计划单ids

    @api.depends('plan_sheet_ids')
    def _compute_task_count(self):
        plan_sheet_count=0 # 任务数
        maintain_sheet_count=0 # 已执行
        for plan in self:
            for plan_sheet in plan.plan_sheet_ids:
                plan_sheet_count += 1
                if plan_sheet.maintain_sheet_id.id: # if plan_sheet.maintain_sheet_no:
                    maintain_sheet_count += 1
            plan.task_count=plan_sheet_count
            plan.executed_count=maintain_sheet_count

    task_count = fields.Integer(default=0, compute='_compute_task_count') # 任务数

    executed_count = fields.Integer(default=0, compute='_compute_task_count') # 已执行

    @api.model
    def create(self, vals):
        # if vals.get('name', 'New') == 'New':
        #     vals['name'] = self.env['ir.sequence'].next_by_code('warranty_plan.order') or 'New'

        # plan_month = datetime.datetime.strftime(datetime.datetime.strptime(vals.get('plan_month'),'%Y-%m-%d %H:%M:%S'), '%Y-%m')
        # vals['month'] = plan_month

        result = super(WarrantyPlan, self.with_context(mail_create_nolog=True)).create(vals)
        result.message_post(body=_('%s has been added to the plan!') % (result.name,))
        return result


