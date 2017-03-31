# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    component_id = fields.Many2one('product.component', string='Product Component')