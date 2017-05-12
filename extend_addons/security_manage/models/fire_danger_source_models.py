# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class fire_danger_source_manage(models.Model):
    _name = 'sfs.fire_danger_src'
    # 危险源名称 string=_('')
    name = fields.Char('source of dange name',required=True)
    # 区域
    area = fields.Char('area',required=True)
    # 位置
    place = fields.Char('place',required=True)
    # 危害性
    risk_evaluate = fields.Char('harmful')
    # risk_evaluate = fields.Text('harmful')
    # 危害描述
    danger_desc = fields.Text('harmful description')
    # 防范措施
    precautions = fields.Text('preventive measures')
