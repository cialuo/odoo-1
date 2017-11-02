# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import models, fields, api

class park_collected_gps_info(models.Model):
    _name = 'park.collected.gps.info'

    name = fields.Integer('name') # 序号
    radius = fields.Integer('radius') # 半径
    azimuth = fields.Integer('azimuth') # 方位角
    longitude = fields.Float(digits=(10, 6), string='longitude') # 经度
    latitude = fields.Float(digits=(10, 6), string='latitude') # 纬度
    park_id = fields.Many2one('opertation_resources_vehicle_yard') #站台ID

class VehicleYard(models.Model):
    """
    站台
    """
    _inherit = 'opertation_resources_vehicle_yard'

    # GPS座标
    gps_ids = fields.One2many('park.collected.gps.info','park_id')

