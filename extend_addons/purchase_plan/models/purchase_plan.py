# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields,exceptions
from odoo.tools.translate import _
from datetime import datetime
import time

class PuchasePlan(models.Model):
    _name = 'purchase.plan'
    _inherit = ['mail.thread']

    @api.model
    def _get_default_user(self):
        """
        根据登录用户获取用户的员工信息
        :return: employee
        """
        user = self.env.user
        if user.employee_ids:
            return user.employee_ids[0].id
        else:
            return False
    @api.model
    def _get_month(self):
        return time.strftime("%Y-%m")




    name = fields.Char(string='name', default='/', readonly=True)
    month = fields.Char(string='Month', readonly=True, states={'draft': [('readonly', False)]}, required=True, default=_get_month)
    user_id = fields.Many2one('hr.employee', string='Create User', required=True, readonly=True,
                              states={'draft': [('readonly', False)]}, default=_get_default_user)
    login_user = fields.Many2one('res.users', string='Login user', default=lambda self: self.env.user)
    sub_company = fields.Many2one('hr.department', related='user_id.department_id', string='User Company', readonly=True)
    user_department = fields.Many2one('hr.department', related='user_id.department_id', string='User Department')
    checker_id = fields.Many2one('hr.employee', string='Check User', readonly=True)
    checker_login = fields.Many2one('res.users')
    checker_department = fields.Many2one('hr.department', related='checker_id.department_id', string='User Department', readonly=True)
    check_date = fields.Datetime(string='Check Date', readonly=True)
    approver_id = fields.Many2one('hr.employee', string='Approve User', readonly=True)
    approve_date = fields.Datetime(string='Approve Date', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submit'), ('confirm', 'Confirm'),
                              ('process', 'Process'), ('done', 'Done')], string='State', default='draft')
    note = fields.Text(string='Note')
    is_run = fields.Boolean(string='Run Procurement?', default=False)
    procurement_group_id = fields.Many2one('procurement.group', string='Proc Group')
    line_ids = fields.One2many('purchase.plan.line', 'plan_id', string='Lines', readonly=True, states={'draft': [('readonly', False)]})
    total = fields.Float(string='Total', compute='_compute_lines',store=True)
    no_suppliers = fields.Integer(string='No supplier', compute='_compute_lines')

    @api.depends('line_ids')
    def _compute_lines(self):
        for order in self:
            order.total = sum([i.sub_total for i in order.line_ids])
            order.no_suppliers = len(order.line_ids.filtered(lambda x: not x.seller_id))

    @api.model
    def create(self, vals):
        """
        自动生成订单号：前缀PPO+年月+序号
        :param vals:
        :return:
        """
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase_plan_seq') or '/'
        res = super(PuchasePlan, self).create(vals)
        return res

    @api.multi
    def unlink(self):
        """
        控制单据的删除，只能删除草稿状态的单据
        :return: 
        """
        for order in self:
            if not order.state == 'draft':
                raise exceptions.UserError(_('In order to delete a purchase plan order, you must set it draft first.'))
        return super(PuchasePlan, self).unlink()

    @api.multi
    def action_submit(self):
        """
        确认提交
        :return:
        """
        for order in self:
            if order.line_ids:
                order.write({'state': 'submit'})
            else:
                raise exceptions.ValidationError(_('Please add lines!'))

    @api.multi
    def action_submit_cancel(self):
        """
        退回重做
        :return:
        """
        self.write({'state': 'draft'})

    @api.multi
    def action_confirm(self):
        """
        审核通过
        :return:
        """
        checker = self._get_default_user()
        self.write({
            'state': 'confirm',
            'checker_id': checker,
            'checker_login': self.env.uid,
            'check_date': datetime.utcnow()
        })

    @api.multi
    def action_confirm_cancel(self):
        """
        退回重审
        :return:
        """
        self.write({'state': 'submit'})

    @api.multi
    def action_process(self):
        """
        审批通过
        :return:
        """
        approver = self._get_default_user()
        self.write({
            'state': 'process',
            'approver_id': approver,
            'approve_date': datetime.utcnow()
        })

    @api.model
    def _prepare_proc_group(self):
        """
        为计划单定义需求组
        :return: dict{} vals of group
        """
        return {'name': self.name}

    @api.multi
    def action_run_procurement(self):
        """
        安排补货
        根据明细创建补货单
        更新明细行的状态，关联的补货单号
        更新计划单为已运行（is_run： True）
        :return:
        """
        for order in self:
            order.line_ids._action_run_procurement()
            order.is_run = True
        return True


class PlanLine(models.Model):
    _name = 'purchase.plan.line'

    product_id = fields.Many2one('product.product', string='Product', ondelete='set null', required=True)
    default_code = fields.Char(related='product_id.default_code', string='Default Code')
    category = fields.Many2one(related='product_id.categ_id')
    barcode = fields.Char(related='product_id.barcode')
    special_attribute = fields.Selection(related='product_id.special_attributes')
    onhand_qty = fields.Float(related='product_id.qty_available')
    virtual_available = fields.Float(related='product_id.virtual_available')
    qty = fields.Float(string='qty', required=True, default=1.0)
    state = fields.Selection([('process', 'Process'), ('running', 'Running'), ('expection', 'Expection'), ('done', 'Done')],
                             related='procurement_id.state', string='Procurement state', readonly=True, store=True)
    procurement_id = fields.Many2one('procurement.order', string='Procurement Order',
                                      ondelete='restrict')
    purchase_id = fields.Many2one('purchase.order', string='Purchase Order', related='procurement_id.purchase_id', ondelete='restrict')
    plan_id = fields.Many2one('purchase.plan', string='Purchase Plan', ondelete='cascade')
    product_tmpl_id = fields.Many2one('product.template')
    seller_id = fields.Many2one('product.supplierinfo', string='Partner', domain="[('product_tmpl_id', '=', product_tmpl_id)]")
    price_unit = fields.Float(string='Price Unit')
    sub_total = fields.Float(string='Sub total', compute='_compute_sub_total', store=True)



    @api.depends('qty', 'price_unit')
    def _compute_sub_total(self):
        for line in self:
            line.sub_total = line.qty * line.price_unit

    @api.onchange('product_id')
    def _onchange_vendor(self):
        """
        根据选择的产品，默认填入该产品的上一次采购供应商
        :return: 
        """
        if self.product_id:
            p_order = self.env['purchase.order.line'].search([('product_id', '=', self.product_id.id)], limit=1,order='id desc')
            p_supplierinfo = self.env['product.supplierinfo'].search([('name', '=', p_order.partner_id.id)], limit=1)
            self.seller_id = p_supplierinfo
            self.product_tmpl_id = self.product_id.product_tmpl_id


    @api.onchange('seller_id')
    def _onchange_price_unit(self):
        """
        根据选择的供应商及产品，提供默认的单价
        :return: 
        """
        if self.seller_id:
            self.price_unit = self.seller_id.price
        else:
            self.price_unit = 0.0


    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        """
        根据计划单明细准备需求单数据

        :param group_id: 需求组
        :return: vals 需求单的数据
        """
        self.ensure_one()
        ws = self.env['stock.warehouse'].search([('buy_to_resupply', '=', True)], limit=1)
        location = ws.lot_stock_id
        return {
            'name': 'XQ-' + self.plan_id.name,
            'origin': self.plan_id.name,
            'product_id': self.product_id.id,
            'product_qty': self.qty,
            'product_uom': self.product_id.uom_id.id,
            'group_id': group_id,
            'location_id': location.id,
        }

    @api.multi
    def _action_run_procurement(self):
        """
        明细行执行对应的需求单
        :return:
        """
        proc_orders = self.env['procurement.order']
        for line in self:
            if not line.plan_id.procurement_group_id:
                vals = line.plan_id._prepare_proc_group()
                line.plan_id.procurement_group_id = self.env['procurement.group'].create(vals)
            vals = line._prepare_order_line_procurement(group_id=line.plan_id.procurement_group_id.id)
            proc_order = self.env['procurement.order'].create(vals)
            line.write({'procurement_id': proc_order.id})
            proc_orders += proc_order
        proc_orders.run()
        return proc_orders

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        """
        库存移动完成时，检查对应需求组是否是采购计划单，并检查计划单的是否全部完成
        :return:
        """
        res = super(StockMove, self).action_done()
        plan_obj = self.env['purchase.plan']
        for move in self:
            if move.procurement_id:
                plan = plan_obj.search([('name', '=', move.procurement_id.origin)])
                if all([a.state == 'done' for a in plan.line_ids]):
                    plan.write({'state': 'done'})
                    # plan.state = 'done'
        return res