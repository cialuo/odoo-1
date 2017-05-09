# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class source_of_danger(models.Model):
    _name = 'srp.source_of_danger'
    # 危险源名称 string=_('')
    name = fields.Char(string='source of dange name')
    # 区域
    area = fields.Char(tring='area')
    # 位置
    place = fields.Char(tring='place')
    # 危害性
    risk_evaluate = fields.Char(string='harmful')
    # 危害描述
    danger_desc = fields.Char(string='harmful description')
    # 防范措施
    precautions = fields.Char(string='preventive measures')
