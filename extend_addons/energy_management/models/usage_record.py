# -*- coding: utf-8 -*-

from odoo import models, fields, api

class usage_record(models.Model):

    _name = 'energy.usage_record'
    _inherit = ['mail.thread']
    _description = 'Energy usage record'

    """
       使用记录
    """

    #能源站
    station_id = fields.Many2one('energy.station',string='Station Id',required=True)

    #能源桩
    pile_id = fields.Many2one('energy.pile',string='Pile Id',domain="[('station_id', '=', station_id)]",required=True)

    #车辆
    vehicle_id = fields.Many2one('fleet.vehicle',string='Vehicle Id',required=True)

    #状态
    state = fields.Selection([('normal', 'Normal'), ('stop', 'Stop')],default='normal')

    #使用
    record_date = fields.Date(string='Record Date')

    #使用人
    user_use = fields.Many2one('res.partner',related='vehicle_id.driver_id',string='User Use')

    #能源型号
    energy_type = fields.Many2one('product.product',string='Energy Type',related='pile_id.energy_type', store=False, readonly=True)

    #能源桩类型
    pile_type = fields.Selection(string='Pile Type', related='pile_id.pile_type', store=False, readonly=True)

    #车牌号
    license_plate = fields.Char(string='License Plate',related='vehicle_id.license_plate', store=False, readonly=True)

    #车辆编号
    inner_code = fields.Char(string='Inner Code',related='vehicle_id.inner_code', store=False, readonly=True)

    #额定油耗
    fuel_capacity = fields.Float(string='Fuel Capacity')

    #单位
    companyc_id = fields.Many2one('product.uom',related='pile_id.companyc_id', store=False, readonly=True,string='Companyc Id')

    #库位
    location_id = fields.Many2one('stock.location', related='pile_id.location_id', store=False, readonly=True,
                                  string='Location Id')

    @api.multi
    def normal_to_stop(self):
        self.state = 'stop'

    @api.multi
    def stop_to_normal(self):
        self.state = 'normal'