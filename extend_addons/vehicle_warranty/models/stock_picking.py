# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError


class Picking(models.Model):
    _inherit = "stock.picking"

    warranty_order_id = fields.Many2one('warranty_order', ondelete='cascade', string="Warranty Order")

    @api.multi
    def action_confirm(self):
        return []
