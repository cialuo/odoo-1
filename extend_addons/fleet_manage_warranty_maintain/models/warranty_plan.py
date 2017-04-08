# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyPlan(models.Model): # 车辆保养计划
    _name = 'fleet_warranty_plan'
    # name = fields.Char()


    name = fields.Char(string='Plan Number', required=True, index=True, default='New') # readonly=True, default=lambda self: 'New' required=True, states={'draft': [('readonly', False)]}, index=True,  copy=False,  self: _('New')

    month = fields.Selection(
        [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'),
         (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=12,
        required=True) #  月度

    #monthly = fields.Datetime(default=fields.Datetime.now) # string='Order Date', required=True, readonly=True, index=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,default=fields.Datetime.now

    company_id = fields.Many2one('res.company', string='Company Id', required=True, default=lambda self: self.env.user.company_id)

    made_company_id = fields.Many2one('res.company', string='Made Company Id', required=True, default=lambda self: self.env.user.company_id)

    auditor_id = fields.Many2one('hr.employee', string="Auditor Id")
    auditor_time = fields.Datetime(string="Auditor Time")

    approval_id = fields.Many2one('hr.employee', string="Approval Id")
    approval_time = fields.Datetime(string="Approval Time")

    remark = fields.Char()

    state = fields.Selection([
        ('draft', 'draft'),
        ('commit', 'commit'),
        ('audit', 'audit'),
        ('execute', 'execute'),
        ('done', 'done'),
    ], readonly=True, default='draft') # copy=False, index=True, track_visibility='onchange',

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_commit(self):
        self.state = 'commit'

    @api.multi
    def action_audit(self):
        self.state = 'audit'

    @api.multi
    def action_execute(self):
        self.state = 'execute'

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
                if plan_sheet.maintain_sheet_no:
                    maintain_sheet_count += 1
            plan.task_count=plan_sheet_count
            plan.executed_count=maintain_sheet_count



    task_count = fields.Integer(default=0, compute='_compute_task_count') # 任务数

    executed_count = fields.Integer(default=0, compute='_compute_task_count') # 已执行




    @api.model
    def create(self, vals):
        # if vals.get('name', 'New') == 'New':
        #     vals['name'] = self.env['ir.sequence'].next_by_code('warranty_plan.order') or 'New'

        # # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        # if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
        #     partner = self.env['res.partner'].browse(vals.get('partner_id'))
        #     addr = partner.address_get(['delivery', 'invoice'])
        #     vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
        #     vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
        #     vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)

        result = super(WarrantyPlan, self).create(vals)
        return result


