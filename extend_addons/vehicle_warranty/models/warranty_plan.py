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

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    month = fields.Char(compute='_compute_month') # 月度

    # company_id = fields.Many2one('hr.department', string='Company', required=True, default=lambda self: self.env.user.company_id)
    #
    # made_company_id = fields.Many2one('hr.department', string='Made Company', required=True, default=lambda self: self.env.user.company_id)

    create_name = fields.Many2one('hr.employee', string="Create Name", default=_default_employee, required=True,
                                  readonly=True)

    company_id = fields.Many2one('hr.department', string='Company', related='create_name.department_id')

    made_company_id = fields.Many2one('hr.department', string='Made Company', related='create_name.department_id')


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
    ], readonly=True, default='draft', string="MyState")

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
        self.auditor_id = self._default_employee()
        self.auditor_time = datetime.datetime.utcnow()

    @api.multi
    def action_execute(self):
        self.state = 'execute'
        self.approval_id = self._default_employee()
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


class WizardWarrantyPlan(models.TransientModel): # 自动生成保养计划
    _name = "wizard_warranty_plan"

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    @api.multi
    def create_warranty_plan(self):
        tmp_plan_month = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m')
        warranty_plan_count=self.env['warranty_plan'].search_count([('month', '=', tmp_plan_month)])
        warranty_plan_count+=1
        company_id=''
        if self._default_employee():
            company_id=self._default_employee().department_id

        warranty_plan_val = {
            'name': 'BYJH'+'-'+tmp_plan_month+'-'+str(warranty_plan_count),  # plan.name + '_' + str(maintain_sheets_count + 1),  # +''+str(maintain_sheets_count)
            'month': tmp_plan_month,
            'company_id': company_id,
            'made_company_id': company_id,
            'state': 'draft'
        }
        warranty_plan = self.env['warranty_plan'].create(warranty_plan_val)

        warranty_plan_order_list = []
        vehicles = self.env['fleet.vehicle'].search([])
        for vehicle in vehicles:
            if vehicle.model_id:
                odometer_count = vehicle.total_odometer
                interval_mileage = 0
                warranty_category_id = 0
                if vehicle.model_id.warranty_interval_ids:
                    for warranty_interval_id in vehicle.model_id.warranty_interval_ids:
                        if odometer_count>warranty_interval_id.interval_mileage:
                            interval_mileage=warranty_interval_id.interval_mileage
                            warranty_category_id = warranty_interval_id.warranty_category_id.id
                    if odometer_count>0 and interval_mileage>0 and warranty_category_id>0:
                        warranty_plan_order_val = {
                            'name': '/',
                            'parent_id': warranty_plan.id,
                            'vehicle_id': vehicle.id,
                            'warranty_category': warranty_category_id,
                            'state': 'draft'
                        }
                        warranty_plan_order_list.append((0, 0, warranty_plan_order_val))

        if len(warranty_plan_order_list) > 0:
            warranty_plan.write({'plan_order_ids': warranty_plan_order_list})

        return False
