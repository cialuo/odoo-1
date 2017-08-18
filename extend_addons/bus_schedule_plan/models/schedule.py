# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime


class route_manage(models.Model):
    """
    线路
    """

    _inherit = 'route_manage.route_manage'

    is_big_rotation = fields.Boolean(default=False) #是否大轮换

    rotation_cycle = fields.Selection([(5, '5days rotation'),
                                       (7, '7days rotation'),
                                       (10, '10days rotation'),
                                       (15, '15days rotation'),
                                       (30, '30days rotation'),
                                       (45, '45days rotation'),
                                       (60, '60days rotation'),
                                       (90, '90days rotation'),
                                       (180, '180days rotation'),
                                       ], string="Rotation Cycle", default=5)         #轮换周期
    last_rotation_date = fields.Date(default=fields.Date.context_today)               #最后轮换时间

    @api.multi
    def write(self, vals):
        if "is_big_rotation" in vals and vals.get('is_big_rotation') or vals.get('rotation_cycle'):
            vals.update({'last_rotation_date': datetime.date.today()})
        return super(route_manage, self).write(vals)
