# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class fire_device_map(models.Model):
    _name = 'sfs.fire_device_map'
    # 分布图名称  string=_('')
    name = fields.Char('fire fight device map name')
    # 区域
    area = fields.Char('area')
    # 位置
    place = fields.Char('place')
    # 制作人 create_uid
    # 上传日期 create_date
    # 附件
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
