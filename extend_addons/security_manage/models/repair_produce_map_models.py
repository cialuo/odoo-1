# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class produce_map(models.Model):
    _name = 'srp.produce_map'
    # 分布图名称
    name = fields.Char(string=_('worksite map name'))
    # 区域  string=_('')
    area = fields.Char(string=_('area'))
    # 位置
    place = fields.Char(string=_('place'))
    # 制作人 create_uid
    # 上传日期create_date
    # 附件
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

