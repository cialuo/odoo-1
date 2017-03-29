# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    component_ids = fields.One2many('product.component', 'parent_vehicle', string='Component')