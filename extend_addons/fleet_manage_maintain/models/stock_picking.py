# -*- coding: utf-8 -*-

from odoo import fields, api, models


class Picking(models.Model):
    _inherit = "stock.picking"

    repair_id = fields.Many2one('fleet_manage_maintain.repair',
                                ondelete='cascade', string="Repair")