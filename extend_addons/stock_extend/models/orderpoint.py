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
from odoo import api, fields, models, exceptions

class OrderPoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.onchange('product_min_qty', 'product_max_qty')
    def _onchange_qty(self):
        if self.product_min_qty > self.product_max_qty:
            raise exceptions.UserError(u'最大数量必须大于最小数量')
    @api.model
    def create(self, vals):
        if vals['product_min_qty'] > vals['product_max_qty']:
            raise exceptions.UserError(u'最大数量必须大于最小数量')
        return super(OrderPoint, self).create(vals)
    @api.multi
    def write(self, vals):
        if vals.get('product_min_qty', self.product_min_qty) > vals.get('product_max_qty', self.product_max_qty):
            raise exceptions.UserError(u'最大数量必须大于最小数量')
        return super(OrderPoint, self).write(vals)