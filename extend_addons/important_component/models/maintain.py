# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import timedelta

class MaintainRepare(models.Model):
    _inherit = 'maintain.repair'



class RepareMethod(models.Model):
    _inherit = 'maintain.fault.method'

    is_important_product = fields.Boolean("Is Important Product")
    important_product_id = fields.Many2one('product.product', string="Important Product",
                                           domain=[('is_important', '=', True)])