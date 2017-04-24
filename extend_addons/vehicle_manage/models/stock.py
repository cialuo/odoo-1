# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_vehicle = fields.Boolean(string='Vehicle', default=False)