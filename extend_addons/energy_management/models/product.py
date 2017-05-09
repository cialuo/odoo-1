# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools
from odoo.modules.module import get_module_resource

class energy_product(models.Model):

     _inherit = ['product.product']

     """
        继承物资，新增
     """

     is_important = fields.Boolean(string='Important', default=False)

     important_type = fields.Selection([('energy', 'Energy')],string='Important Type')


