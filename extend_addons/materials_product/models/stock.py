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

class StockMove(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_confirm(self):
        #自动根据operation中的自动生成批次号,并写入完成数
        res = super(StockMove, self).action_confirm()
        for picking in self:
            if picking.picking_type_id.code == 'incoming':
                if picking.pack_operation_ids:
                    lot_obj = self.env['stock.pack.operation.lot']
                    for p in picking.pack_operation_ids:
                        if p.product_id.tracking == 'lot' and p.product_id.auto_lot:
                            lot_name = self.env['ir.sequence'].next_by_code('lot_name_seq') or '/'
                            vals = {
                                'lot_name': lot_name,
                                'qty': p.product_qty,
                                'operation_id': p.id,
                            }
                            lot_obj.create(vals)
                            p.qty_done = p.product_qty
        return res
# class OperationLot(models.Model):
#     _inherit = 'stock.pack.operation.lot'
#
#     @api.model
#     def create(self, vals):
#         if not vals.get('lot_name'):
#             lot_name = self.env['ir.sequence'].next_by_code('lot_name_seq') or '/'
#             vals['lot_name'] = lot_name
#         res = super(OperationLot, self).create(vals)
#         return res