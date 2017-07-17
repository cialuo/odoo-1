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
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class MultiProduct(models.TransientModel):
    _name = 'multi.product.wizard'

    product_id = fields.Many2many('product.product', string='Materials Product')

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        if self._context.get('active_id'):
            order = self.env['purchase.order'].browse(self._context['active_id'])
            lines = []
            for p in self.product_id:
                name = p.name_get()[0][1]
                if p.description_purchase:
                    name += '\n' + p.description_purchase
                vals = {
                    'product_id': p.id,
                    'product_qty': 1,
                    'product_uom': p.uom_id.id,
                    'price_unit': 0.0,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'name': name,
                }
                lines.append((0,0,vals))
            order.write({'order_line': lines})