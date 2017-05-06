# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class fire_device_manage(models.Model):
    _name = 'sfs.fire_device_manage'
    # 设备名称 string=_('')
    name = fields.Char(string=_('fire device name'))
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
    owner = fields.Char(string=_('fire device owner'))
    # 保养团队
    maintenance_team = fields.Char(string=_('fire device mainten team'))
    # 技术员
    technician = fields.Char(string=_('fire device technician'))
    # 使用位置
    use_position = fields.Char(string=_('fire device use position'))
    # 分派日期
    dispatch_date = fields.Date(string=_('fire device dispatch date'))
    # 序列号
    serial_number = fields.Char(string=_('device serial number'))
    # 报废日期
    scrap_date = fields.Date(string=_('device scrap date'))
    # 说明
    description = fields.Text(string=_('device description'))
    # 产品信息
    product_info = fields.Text(string=_('device information'))
    # 保养
    maintenance = fields.Text(string=_('device mainten desc'))
