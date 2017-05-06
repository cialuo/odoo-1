# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class produce_map(models.Model):
    _name = 'srp.produce_map'
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
