# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyMaintainSheet(models.Model): # 保养单
    _name = 'fleet_manage_warranty_maintain.warranty_maintain_sheet'
    name = fields.Char()

    state = fields.Selection([ # 状态
        ('draft', "draft"),
        ('confirmed', "confirmed"),
        ('done', "done"),
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

    vehicle_no = fields.Char()  # 车号
    vehicle_type = fields.Char()  # 车型

    #plansheet_id = fields.Many2one('fleet_manage_warranty_maintain.warranty_plan_sheet', 'plansheetId', required=True, ondelete='cascade') # 保养计划单号

    plan_id = fields.Many2one('fleet_manage_warranty_maintain.warranty_plan', 'planId', required=True, ondelete='cascade')  # 保养计划号

    warrantycategory_id = fields.Many2one('fleet_manage_warranty.category', 'Category', ondelete="set null") # 保养类别

    item_ids = fields.One2many('fleet_manage_warranty_maintain.maintain_sheet.item', 'maintainsheet_id', 'maintainsheetId', copy=True)


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('warranty_plan.order') or 'New'

        # # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        # if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
        #     partner = self.env['res.partner'].browse(vals.get('partner_id'))
        #     addr = partner.address_get(['delivery', 'invoice'])
        #     vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
        #     vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
        #     vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)

        result = super(WarrantyMaintainSheet, self).create(vals)
        return result


class MaintainSheetItem(models.Model): # 保养单_保养项目
    _name = 'fleet_manage_warranty_maintain.maintain_sheet.item'
    _order = "sequence"
    #_rec_name = "product_id"

    # def _get_default_product_uom_id(self):
    #     return self.env['product.uom'].search([], limit=1, order='id').id

    # product_id = fields.Many2one(
    #     'product.product', 'Product', required=True)


    sequence = fields.Integer(
        'Sequence', default=1,
        help="Gives the sequence order when displaying.")


    maintainsheet_id = fields.Many2one('fleet_manage_warranty_maintain.warranty_maintain_sheet', index=True)


    # product_qty = fields.Float(
    #     'Product Quantity', default=1.0,
    #     digits=dp.get_precision('Product Unit of Measure'), required=True)

    # product_uom_id = fields.Many2one(
    #     'product.uom', 'Product Unit of Measure',
    #     default=_get_default_product_uom_id,
    #     oldname='product_uom', required=True,
    #     help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control")

    maintenance_part = fields.Char()  # 保养部位
    category_id = fields.Many2one('fleet_manage_warranty.category') # 保养类别
    item_id = fields.Many2one('fleet_manage_warranty.item', 'Item', required=True) # 保养项目
    maintenance_method = fields.Char()  # 保养办法
    maintenance_personnel = fields.Char()  # 保养人员
    state = fields.Selection([ # 状态
        ('nodispatch', "nodispatch"),
        ('dispatch', "dispatch"),
        ('maintain', "maintain"),
        ('check', "check"),
        ('complete', "complete"),
    ], default='nodispatch')

    inspection_operation = fields.Selection([ # 报检操作
        ('noinspection', "noinspection"),
        ('inspection', "inspection"),
    ], default='noinspection')

    reinspection_count = cost_count = fields.Integer(string="ReinspectionCount")  # 重检验次数 compute="_compute_count_all",