# -*- coding: utf-8 -*-
##############################################################################
#
#
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
from odoo import api, fields, models, _

class PartnerType(models.Model):
    _name = 'partner.type'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    """
    供应商类型
    """
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string='Code')
    parent_id = fields.Many2one('partner.type', string='Partner Type')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)
    note = fields.Char(string='Note')
    state = fields.Selection([('inuse', 'Inuse'), ('inactive', 'Inactive')], default='inuse')
    active = fields.Boolean(default=True, string="Active")

    # @api.multi
    # def name_get(self):
    #     def get_names(cat):
    #         """ Return the list [cat.name, cat.parent_id.name, ...] """
    #         res = []
    #         while cat:
    #             res.append(cat.name)
    #             cat = cat.type_id
    #         return res
    #
    #     return [(cat.id, "".join(reversed(get_names(cat)))) for cat in self]

    @api.multi
    def action_active(self):
        return self.write({'active': True, 'state': 'inuse'})
    @api.multi
    def action_inactive(self):
        return self.write({'active': False, 'state': 'inactive'})

class Partner(models.Model):
    _inherit = 'res.partner'

    survey_file = fields.Many2many('ir.attachment', 'partner_attachment_rel', string="Attachment")
    product_info_ids = fields.One2many('product.supplierinfo', 'name', string='Product Supplier')
    product_info_count = fields.Integer(compute='_count_product_info')
    picking_return_count = fields.Integer(compute='_count_picking_return')
    partner_type_id = fields.Many2one('partner.type', string='Type')

    @api.multi
    def _count_product_info(self):
        """
        计算供应商对应的所有供货信息
        :return: 
        """
        supplier = self.env['product.supplierinfo']
        for partner in self:
            if supplier.search([('name', '=', partner.id)]):
                partner.product_info_count = len(supplier.search([('name', '=', partner.id)]))

    @api.multi
    def _count_picking_return(self):
        """
        计算供应商对应的退货单
        :return: 
        """
        picking = self.env['stock.picking']
        for partner in self:
            return_picking = picking.search([('is_return', '=', True), ('partner_id', '=', partner.id)])
            if return_picking:
                partner.picking_return_count = len(return_picking)

    @api.multi
    def action_picking(self):
        """
        打开供应商对应的退货单tree视图
        :return: 
        """
        action = self.env.ref('stock.action_picking_tree')
        picking = self.env['stock.picking']
        result = action.read()[0]
        result['context'] = {}
        for partner in self:
            return_picking = picking.search([('is_return', '=', True), ('partner_id', '=', partner.id)])
            if len(return_picking):
                result['domain'] = [('id', 'in', return_picking.ids)]
        return result




class Picking(models.Model):
    _inherit = 'stock.picking'

    #增加 单据 退货标记
    is_return = fields.Boolean(default=False, string='Is return')

class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    @api.multi
    def create_returns(self):
        for wizard in self:
            new_picking_id, pick_type_id = wizard._create_returns()
            self.env['stock.picking'].browse(new_picking_id).write({'is_return': True})
        # Override the context to disable all the potential filters that could have been set previously
        ctx = dict(self.env.context)
        ctx.update({
            'search_default_picking_type_id': pick_type_id,
            'search_default_draft': False,
            'search_default_assigned': False,
            'search_default_confirmed': False,
            'search_default_ready': False,
            'search_default_late': False,
            'search_default_available': False,
        })
        return {
            'name': _('Returned Picking'),
            'view_type': 'form',
            'view_mode': 'form,tree,calendar',
            'res_model': 'stock.picking',
            'res_id': new_picking_id,
            'type': 'ir.actions.act_window',
            'context': ctx,
        }