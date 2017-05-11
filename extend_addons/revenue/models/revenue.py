# -*- coding: utf-8 -*-

from odoo import models, fields, api

class coin_revenue(models.Model):
    _name = 'coin_revenue.coin_revenue'
    _rec_name = 'route'

    # 日期 线路 车牌号 驾驶员 投币收入（元）备注
    c_date = fields.Date('Date')
    route = fields.Char('Route', required=True)
    license_plate = fields.Char('License plate', required=True)
    driver = fields.Char('Driver')
    revenue = fields.Float(digits=(10, 2), string='Coin income（CNY）')
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', 'The route must be unique!'),
        ('license_plate_unique', 'unique(license_plate)', 'The license plate must be unique!'),
    ]

class ic_revenue(models.Model):
    _name = "ic_revenue.ic_revenue"
    _rec_name = 'route'

    #车牌号 驾驶员 收入 备注
    c_date = fields.Date('Date')
    route = fields.Char('Route', required=True)
    license_plate = fields.Char('License plate', required=True)
    driver = fields.Char('Driver')
    revenue = fields.Float(digits=(10, 2), string='IC income（CNY）')
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', 'The route must be unique!'),
        ('license_plate_unique', 'unique(license_plate)', 'The license plate must be unique!'),
    ]

class chartered_revenue(models.Model):
    _name = "chartered_revenue.chartered_revenue"
    _rec_name = 'route'

    #车牌号 驾驶员 收入 备注 包车
    c_date = fields.Date('Date')
    route = fields.Char('Route', required=True)
    license_plate = fields.Char('License plate', required=True)
    driver = fields.Char('Driver')
    revenue = fields.Float(digits=(10, 2), string='Chartered income（CNY）')
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', 'The route must be unique!'),
        ('license_plate_unique', 'unique(license_plate)', 'The license plate must be unique!'),
    ]


class total_revenue(models.Model):
    _name = "total_revenue.total_revenue"

    _rec_name = 'route'
    #车牌号 驾驶员 总收入 备注 包车
    c_date = fields.Date('Date')
    route = fields.Char('Route', required=True)
    license_plate = fields.Char('License plate', required=True)
    driver = fields.Char('Driver')
    coin_revenue = fields.Float(digits=(10, 2), string='Coin income（CNY）')
    ic_revenue = fields.Float(digits=(10, 2), string='IC income（CNY）')
    chartered_revenue = fields.Float(digits=(10, 2), string='Chartered income（CNY）')
    total_income = fields.Float(digits=(10, 2), string='Total Income（CNY）')
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', 'The route must be unique!'),
        ('license_plate_unique', 'unique(license_plate)', 'The license plate must be unique!'),
    ]
