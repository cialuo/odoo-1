# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class total_revenue(models.Model):

    _name = "total_revenue"

    _rec_name = 'route'

    # 获取车牌号，暂未用
    @api.depends('route')
    def _getVehicleNumber(self):
        res = self.env['fleet.vehicle'].search([])
        for item in res:
            print '========%s'%item.license_plate

    # @api.multi
    # def _set_license_plate(self, route):

    # 计算费用总额
    @api.depends('coin_revenue', 'ic_revenue', 'chartered_revenue')
    def _getTotalAmount(self):
        for record in self:
            record.total_income = record.coin_revenue + record.ic_revenue + record.chartered_revenue

    # 日期
    c_date = fields.Date('Date')
    # 线路
    route = fields.Many2one('route_manage.route_manage', string='Route', required=True)
    # 车辆编号
    vehicle_number = fields.Many2one('fleet.vehicle', string='Vehicle number', required=True)
    # 车牌号
    license_plate = fields.Char(related='vehicle_number.license_plate', string='License plate', readonly=True)
    # 驾驶员
    driver = fields.Char('Driver')
    # 投币收入（元）
    coin_revenue = fields.Float(digits=(10, 2), string='Coin income（CNY）')
    # IC卡收入（元）
    ic_revenue = fields.Float(digits=(10, 2), string='IC income（CNY）')
    # 包车收入（元）
    chartered_revenue = fields.Float(digits=(10, 2), string='Chartered income（CNY）')
    # 合计营收（元）
    total_income = fields.Float(digits=(10, 2), string='Total Income（CNY）', compute='_getTotalAmount')
    # 备注
    remark = fields.Text('Remark')

    # sql 约束，效率高
    _sql_constraints = [
        ('route_unique', 'unique(route)', _('The route must be unique!')),
        ('license_plate_unique', 'unique(license_plate)', _('The license plate must be unique!')),
    ]

class coin_revenue(models.Model):
    _inherit = 'total_revenue'

class ic_revenue(models.Model):
    _inherit = 'total_revenue'

class chartered_revenue(models.Model):
    _inherit = 'total_revenue'


