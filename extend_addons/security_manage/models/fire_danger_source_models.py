# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class fire_danger_source_manage(models.Model):
    _name = 'sfs.fire_danger_src'
    # 危险源名称 string=_('')
    name = fields.Char(string=_('source of dange name'))
    # 区域
    area = fields.Char(string=_('area'))
    # 位置
    place = fields.Char(string=_('place'))
    # 危害性
    risk_evaluate = fields.Char(string=_('harmful'))
    # 危害描述
    danger_desc = fields.Char(string=_('harmful description'))
    # 防范措施
    precautions = fields.Char(string=_('preventive measures'))
