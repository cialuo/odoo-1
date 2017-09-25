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

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    picking_type_id = fields.Many2one(readonly=True, states={'draft': [('readonly', False)]})

#显示买进成本和平均成本
class StockQuant(models.Model):
    _inherit = 'stock.quant'

    cost_purchase = fields.Float(compute='get_cost', string="Cost purchase")
    cost_average = fields.Float(compute='get_cost', string="Cost average")


    @api.multi
    def get_cost(self):
        for quant in self:
            quant.cost_average = quant.product_id.standard_price
            #不管理批次的话，则采购成本为平均成本
            if not quant.lot_id:
                quant.cost_purchase = quant.product_id.standard_price
            else:
                move_ids = quant.lot_id.mapped('quant_ids').mapped('history_ids')
                income_move = move_ids.filtered(lambda x: x.picking_type_id.code == 'incoming')
                #如果由采购入库的则取采购价格，如果是盘点入库的，则采购成本为平均成本
                if income_move:
                    quant.cost_purchase = income_move[0].price_unit
                else:
                    quant.cost_purchase = quant.product_id.standard_price