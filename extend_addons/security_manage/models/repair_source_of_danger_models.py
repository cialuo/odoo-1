# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class source_of_danger(models.Model):
    _name = 'srp.source_of_danger'
    # 危险源名称
    name = fields.Char()
    # 区域
    area = fields.Char()
    # 位置
    place = fields.Char()
    # 危害性
    risk_evaluate = fields.Char()
    # 危害描述
    danger_desc = fields.Char()
    # 防范措施
    precautions = fields.Char()

