# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from lxml import etree
from datetime import datetime

class Product(models.Model):
    _inherit = 'product.product'

    """
     扩展产品模块，定义重要部件
     重要部件会包含：适用车型，交旧领新，退役寿命，里程数
     """
    special_attributes = fields.Selection([('common', 'Common'), ('special', 'Special'), ('general', 'General')],
                                          default='common', string='Special Attribute')