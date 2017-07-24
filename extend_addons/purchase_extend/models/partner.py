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
from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    survey_file = fields.Many2many('ir.attachment', 'partner_attachment_rel', string="Attachment")
    partner_type = fields.Many2one('partner.type', string="Type")
    # product_info_ids = fields.One2many('product.supplierinfo', 'name', string='Product Supplier')
    product_info_count = fields.Integer(compute='_count_product_info')
    # picking_return_ids = fields.One2many('stock.picking', 'partner_id', string='Return Picking')
    picking_return_count = fields.Integer(compute='_count_picking_return')

    @api.multi
    def _count_product_info(self):
        supplier = self.env['product.supplierinfo']
        for partner in self:
            if supplier.search([('name', '=', partner.id)]):
                partner. product_info_count = len(supplier.search([('name', '=', partner.id)]))
    def _count_picking_return(self):
        picking = self.env