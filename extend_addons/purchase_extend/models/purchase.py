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

class Purchase_line(models.Model):
    _inherit = 'purchase.order.line'

    qty_received = fields.Float(compute='compute_qty_received')

    @api.depends('order_id.state', 'move_ids')
    def compute_qty_received(self):
        for line in self:
            if line.order_id.state not in ['purchase', 'done']:
                line.qty_received = 0.0
                continue
            if line.product_id.type not in ['consu', 'product']:
                line.qty_received = line.product_qty
                continue
            total = 0.0
            for move in line.move_ids:
                if move.state == 'done':
                    if not move.picking_id.is_return:
                        if move.product_uom != line.product_uom:
                            total += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
                        else:
                            total += move.product_uom_qty
                    else:
                        if move.product_uom != line.product_uom:
                            total -= move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
                        else:
                            total -= move.product_uom_qty
            line.qty_received = total

    date_planned = fields.Datetime(required=False)
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        for order in self:
            if any([ptype in ['product', 'consu'] for ptype in order.order_line.mapped('product_id.type')]):
                pickings = order.picking_ids.filtered(lambda x: x.state not in ('done','cancel'))
                if not pickings:
                    res = order._prepare_picking()
                    picking = StockPicking.create(res)
                else:
                    picking = pickings[0]
                moves = order.order_line._create_stock_moves(picking)
                # moves = moves.action_confirm()
                # moves.force_assign()
                picking.message_post_with_view('mail.message_origin_link',
                    values={'self': picking, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return True