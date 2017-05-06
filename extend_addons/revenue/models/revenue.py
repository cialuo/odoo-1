# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class coin_revenue(models.Model):
    _name = 'coin_revenue.coin_revenue'
    _rec_name = 'route'

    # 日期 线路 车牌号 驾驶员 投币收入（元）备注
    c_date = fields.Date(_('Date'))
    route = fields.Char(_('Route'), required=True)
    license_plate = fields.Char(_('License plate'), required=True)
    driver = fields.Char(_('Driver'))
    revenue = fields.Float(digits=(10, 2), string=_('Coin income（CNY）'))
    remark = fields.Text(_('Remark'))

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', _('The route must be unique!')),
        ('license_plate_unique', 'unique(license_plate)', _('The license plate must be unique!')),
    ]

class ic_revenue(models.Model):
    _name = "ic_revenue.ic_revenue"
    _rec_name = 'route'

    #车牌号 驾驶员 收入 备注
    c_date = fields.Date(_('Date'))
    route = fields.Char(_('Route'), required=True)
    license_plate = fields.Char(_('License plate'), required=True)
    driver = fields.Char(_('Driver'))
    revenue = fields.Float(digits=(10, 2), string=_('IC income（CNY）'))
    remark = fields.Text(_('Remark'))

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', _('The route must be unique!')),
        ('license_plate_unique', 'unique(license_plate)', _('The license plate must be unique!')),
    ]

class chartered_revenue(models.Model):
    _name = "chartered_revenue.chartered_revenue"
    _rec_name = 'route'

    #车牌号 驾驶员 收入 备注 包车
    c_date = fields.Date(_('Date'))
    route = fields.Char(_('Route'), required=True)
    license_plate = fields.Char(_('License plate'), required=True)
    driver = fields.Char(_('Driver'))
    revenue = fields.Float(digits=(10, 2), string=_('Chartered income（CNY）'))
    remark = fields.Text(_('Remark'))

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', _('The route must be unique!')),
        ('license_plate_unique', 'unique(license_plate)', _('The license plate must be unique!')),
    ]


class total_revenue(models.Model):
    _name = "total_revenue.total_revenue"

    _rec_name = 'route'
    #车牌号 驾驶员 总收入 备注 包车
    c_date = fields.Date(_('Date'))
    route = fields.Char(_('Route'), required=True)
    license_plate = fields.Char(_('License plate'), required=True)
    driver = fields.Char(_('Driver'))
    coin_revenue = fields.Float(digits=(10, 2), string=_('Coin income（CNY）'))
    ic_revenue = fields.Float(digits=(10, 2), string=_('IC income（CNY）'))
    chartered_revenue = fields.Float(digits=(10, 2), string=_('Chartered income（CNY）'))
    total_income = fields.Float(digits=(10, 2), string=_('Total Income（CNY）'))
    remark = fields.Text(_('Remark'))

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', _('The route must be unique!')),
        ('license_plate_unique', 'unique(license_plate)', _('The license plate must be unique!')),
    ]
