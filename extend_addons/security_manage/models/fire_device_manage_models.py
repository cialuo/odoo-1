# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class fire_device_manage(models.Model):
    _name = 'sfs.fire_device_manage'
    # 设备名称 string=_('')
    name = fields.Char('fire device name')
    # 设备分类
    device_category = fields.Selection([
        ('fire_fight_device', 'Fire fight device'),
        ('general_device','General  device'),
        ('profession_device', 'Profession device'),
        ('work_device', 'Work device'),
        ('checkout_device', 'Checkout device'),
        ('information_device', 'Information device')
    ],string='device_category')

    # 所有者
    owner = fields.Char('fire device owner')
    # 保养团队
    maintenance_team = fields.Char('fire device mainten team')
    # 技术员
    technician = fields.Char('fire device technician')
    # 使用位置
    use_position = fields.Char('fire device use position')
    # 分派日期
    dispatch_date = fields.Date('fire device dispatch date')
    # 序列号
    serial_number = fields.Char('device serial number')
    # 报废日期
    scrap_date = fields.Date('device scrap date')
    # 说明
    description = fields.Text('device description')
    # 产品信息
    product_info = fields.Text('device information')
    # 保养
    maintenance = fields.Text('device mainten desc')
