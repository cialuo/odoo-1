# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class total_revenue(models.Model):

    _name = "total_revenue"

    _rec_name = 'license_plate'

    # 日期
    c_date = fields.Date('Date', required=True)

    # 车辆编号
    vehicle_id = fields.Many2one('fleet.vehicle', required=True)
    # 车牌号
    license_plate = fields.Char(related='vehicle_id.license_plate', string='License plate', readonly=True)
    # 线路
    route_id = fields.Many2one('route_manage.route_manage',related='vehicle_id.route_id',  string='Route', readonly=True)

    # 驾驶员
    driver_ids = fields.Many2many('hr.employee', related='vehicle_id.driver', string="driver")
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
        ('license_plate_unique', 'unique(vehicle_id,c_date)', _('The data must be unique!')),
    ]


    # 计算费用总额
    @api.depends('coin_revenue', 'ic_revenue', 'chartered_revenue')
    def _getTotalAmount(self):
        for record in self:
            record.total_income = record.coin_revenue + record.ic_revenue + record.chartered_revenue

class coin_revenue(models.Model):
    _inherit = 'total_revenue'

class ic_revenue(models.Model):
    _inherit = 'total_revenue'

class chartered_revenue(models.Model):
    _inherit = 'total_revenue'


