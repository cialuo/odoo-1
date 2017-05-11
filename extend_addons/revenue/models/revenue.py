# -*- coding: utf-8 -*-

from odoo import models, fields, api

class coin_revenue(models.Model):

    _name = 'coin_revenue.coin_revenue'

    _rec_name = 'route'

    # 日期
    c_date = fields.Date('Date')
    # 线路
    route = fields.Char('Route', required=True)
    # 车牌号
    license_plate = fields.Char('License plate', required=True)
    # 驾驶员
    driver = fields.Char('Driver')
    # 投币收入（元）
    revenue = fields.Float(digits=(10, 2), string='Coin income（CNY）')
    # 备注
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', 'The route must be unique!'),
        ('license_plate_unique', 'unique(license_plate)', 'The license plate must be unique!'),
    ]

class ic_revenue(models.Model):

    _name = "ic_revenue.ic_revenue"

    _rec_name = 'route'

    # 日期
    c_date = fields.Date('Date')
    # 线路
    route = fields.Char('Route', required=True)
    # 车牌号
    license_plate = fields.Char('License plate', required=True)
    # 驾驶员
    driver = fields.Char('Driver')
    # IC卡收入（元）
    revenue = fields.Float(digits=(10, 2), string='IC income（CNY）')
    # 备注
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', 'The route must be unique!'),
        ('license_plate_unique', 'unique(license_plate)', 'The license plate must be unique!'),
    ]

class chartered_revenue(models.Model):

    _name = "chartered_revenue.chartered_revenue"

    _rec_name = 'route'

    # 日期
    c_date = fields.Date('Date')
    # 线路
    route = fields.Char('Route', required=True)
    # 车牌号
    license_plate = fields.Char('License plate', required=True)
    # 驾驶员
    driver = fields.Char('Driver')
    # 包车收入（元）
    revenue = fields.Float(digits=(10, 2), string='Chartered income（CNY）')
    # 备注
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', 'The route must be unique!'),
        ('license_plate_unique', 'unique(license_plate)', 'The license plate must be unique!'),
    ]

class total_revenue(models.Model):

    _name = "total_revenue.total_revenue"

    _rec_name = 'route'

    # 日期
    c_date = fields.Date('Date')
    # 线路
    route = fields.Char('Route', required=True)
    # 车牌号
    license_plate = fields.Char('License plate', required=True)
    # 驾驶员
    driver = fields.Char('Driver')
    # 投币收入（元）
    coin_revenue = fields.Float(digits=(10, 2), string='Coin income（CNY）')
    # IC卡收入（元）
    ic_revenue = fields.Float(digits=(10, 2), string='IC income（CNY）')
    # 包车收入（元）
    chartered_revenue = fields.Float(digits=(10, 2), string='Chartered income（CNY）')
    # 合计营收（元）
    total_income = fields.Float(digits=(10, 2), string='Total Income（CNY）')
    # 备注
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', 'The route must be unique!'),
        ('license_plate_unique', 'unique(license_plate)', 'The license plate must be unique!'),
    ]
