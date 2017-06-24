# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    pick_user = fields.Many2one('res.users', string='Pick User', default=lambda self: self.env.uid,
                                readonly=True, states={'draft': [('readonly', False)]})