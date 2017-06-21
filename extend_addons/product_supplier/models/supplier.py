# -*- coding: utf-8 -*-
##############################################################################
#
#    product supplier
#    Copyright (C) 2017 xiao (715294035@qq.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.
#
##############################################################################
from odoo import models, api, fields, exceptions, _

class Supplier(models.Model):
    _name = 'supplier.order'
    _order = 'id desc'

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

    name = fields.Char(string='Name', default='/')
    partner_id = fields.Many2one('res.partner', required=True, readonly=True, states={'draft': [('readonly', False)]})
    user_id = fields.Many2one('res.users', default=lambda self:self.env.uid)
    employee_id = fields.Many2one('hr.employee', default=_get_default_user, readonly=True, states={'draft': [('readonly', False)]})
    ref = fields.Char(string='Ref')
    line_ids = fields.One2many('supplier.order.line', 'order_id', string='Lines', readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('done', 'Done')], string='State', default='draft')

    @api.model
    def create(self, vals):
        """
        自动生成报价单单号： QT+两位数年份+日期+序号
        :param vals: 
        :return: 
        """
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('supplier_order_seq') or '/'
        res = super(Supplier, self).create(vals)
        return res
    @api.multi
    def unlink(self):
        """
        控制单据的删除，只能删除草稿状态的单据
        :return: 
        """
        for order in self:
            if not order.state == 'draft':
                raise exceptions.UserError(_('In order to delete a supplier order, you must set it draft first.'))
        return super(Supplier, self).unlink()


    @api.multi
    def action_submit(self):
        """
        提交按钮
        :return: 
        """
        for order in self:
            if not order.line_ids:
                raise exceptions.UserError(_('No lines to submit!'))
        self.write({'state': 'submitted'})
    @api.multi
    def action_done(self):
        """
        审核按钮
        同一个产品同一个供应商的话，则只修改最小数量及单价，
        不存在的话，则新建一个供应商信息
        :return: 
        """
        for order in self:
            for line in order.line_ids:
                tmpl = line.product_id.product_tmpl_id
                supplier = self.env['product.supplierinfo']
                available_supplier = supplier.search([('product_tmpl_id', '=', tmpl.id), ('name', '=', order.partner_id.id)], limit=1)
                vals = {
                    'min_qty': line.qty,
                    'price': line.price_unit,
                }
                if available_supplier:
                    available_supplier.write(vals)
                else:
                    vals.update({
                        'name': order.partner_id.id,
                        'product_tmpl_id': tmpl.id,
                    })
                    supplier.create(vals)
        self.write({'state': 'done'})

class SupplierLines(models.Model):
    _name = 'supplier.order.line'

    order_id = fields.Many2one('supplier.order', string='Supplier Order')
    product_id = fields.Many2one('product.product', string='Materials Product', required=True)
    categ_id = fields.Many2one(related='product_id.categ_id', string='Materials Category')
    qty = fields.Float(string='Order Qty')
    price_unit = fields.Float(string='Order Price')
    uom_id = fields.Many2one('product.uom')

    @api.onchange('product_id')
    def _onchange_uom(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_po_id