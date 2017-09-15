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

class MultiLot(models.TransientModel):
    _name = 'multi.lot.wizard'

    tracking = fields.Selection([('none', 'None'), ('lot', 'Lot'), ('serial', 'Serial')], string="Tracking", default='lot')
    all_product = fields.Boolean(string="All Product", default=True)

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        products = self.env['product.product'].search([('type', '=', 'product')])
        products.write({'tracking': self.tracking, 'auto_lot': True})
        return True