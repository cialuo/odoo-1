# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class fire_device_manage(models.Model):
    _name = 'sfs.fire_device_manage'
    # 设备名称
    name = fields.Char()
    # 设备分类
    device_category = fields.Selection([
        ('fire_fight_device', _('Fire fight device')),
        ('general_device', _('General  device')),
        ('profession_device', _('Profession device')),
        ('work_device', _('Work device')),
        ('checkout_device', _('Checkout device')),
        ('information_device', _('Information device'))
    ], string=_('device_category'))

    # 所有者
    owner = fields.Char()
    # 保养团队
    maintenance_team = fields.Char()
    # 技术员
    technician = fields.Char()
    # 使用位置
    use_position = fields.Char()
    # 分派日期
    dispatch_date = fields.Date()
    # 序列号
    serial_number = fields.Char()
    # 报废日期
    scrap_date = fields.Date()
    # 说明
    description = fields.Text()
    # 产品信息
    product_info = fields.Text()
    # 保养
    maintenance = fields.Text()
