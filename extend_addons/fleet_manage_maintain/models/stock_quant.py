# -*- coding: utf-8 -*-

from odoo import fields, api, models


class Quant(models.Model):
    _inherit = "stock.quant"

    def _quants_get_reservation(self, quantity, move, ops=False, domain=None, **kwargs):
        domain = domain if domain is not None else [('qty', '>', 0.0)]
        domain.append([('is_vehicle', '=', False), ('scrap_location', '=', False)])
        return super(Quant, self)._quants_get_reservation(quantity, move, ops, domain, **kwargs)