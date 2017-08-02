# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime


class route_manage(models.Model):
    """
    线路
    """

    _inherit = 'route_manage.route_manage'

    is_big_rotation = fields.Boolean(default=False)

    rotation_cycle = fields.Selection([(5, '5days rotation'),
                                       (7, '7days rotation'),
                                       (10, '10days rotation'),
                                       (15, '15days rotation'),
                                       (30, '30days rotation'),
                                       (45, '45days rotation'),
                                       (60, '60days rotation'),
                                       (90, '90days rotation'),
                                       (180, '180days rotation'),
                                       ], string="Calculate State", default=5)