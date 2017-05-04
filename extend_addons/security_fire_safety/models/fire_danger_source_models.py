# -*- coding: utf-8 -*-

from odoo import models, fields, api


class fire_danger_source_manage(models.Model):
    _name = 'sfs.fire_danger_src'
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
