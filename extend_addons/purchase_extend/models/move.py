# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, exceptions

class move(models.Model):

    _inherit = 'stock.move'

    """
        继承库存移动：
            保存picking单据的is_return
    """

    is_return = fields.Boolean(default=False, string='Is return',related = 'picking_id.is_return',store = True)