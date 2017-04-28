# -*- coding: utf-8 -*-

from odoo import models, fields, api


class warehouse_location(models.Model):

    _inherit = ['stock.location']

    """
       继承库位
    """

    # 能源站
    station_id = fields.Many2one('energy.station', string='Station Id',domain="[('state', '=', 'normal')]")

    #能源站编号
    station_no = fields.Char(string='Station No', related='station_id.station_no', store=False, readonly=True)

    #库位编号
    location_no = fields.Char(string='Location No')

    #库位容量
    location_capacity = fields.Float(string='Location Capacity')

    #库位状态
    state = fields.Selection([('normal','Normal'),('stop','Stop')],default='normal')

    # 能源类型
    energy_type = fields.Many2one('product.product',string='Energy Type',domain="[('important_type', '=', 'energy')]")

    @api.multi
    def normal_to_stop(self):
        self.state = 'stop'

    @api.multi
    def stop_to_normal(self):
        self.state = 'normal'
