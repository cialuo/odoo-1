# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyPlan(models.Model): # 车辆保养计划
    _name = 'fleet_manage_warranty_maintain.warranty_plan'
    # name = fields.Char()


    name = fields.Char(string='Order Reference', readonly=True, default=lambda self: 'New') # required=True, states={'draft': [('readonly', False)]}, index=True,  copy=False,  self: _('New')

    monthly = fields.Datetime(default=fields.Datetime.now) # string='Order Date', required=True, readonly=True, index=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,default=fields.Datetime.now

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

    plan_sheet_ids = fields.One2many('fleet_manage_warranty_maintain.warranty_plan_sheet', 'parent_id', 'sheetIds', copy=True)


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

        result = super(WarrantyPlan, self).create(vals)
        return result


