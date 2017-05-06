# -*- coding: utf-8 -*-

from odoo import models, fields, api


class fire_device_map(models.Model):
    _name = 'sfs.fire_device_map'
    # 分布图名称
    name = fields.Char()
    # 区域
    area = fields.Char()
    # 位置
    place = fields.Char()
    # 制作人
    creator = fields.Char()
    # 上传日期
    update_date = fields.Date()
