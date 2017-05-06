# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
from odoo.exceptions import UserError
import time


class FleetVehicle(models.Model):
    """
    车辆档案
    """
    _inherit = "fleet.vehicle"

    # 抛锚记录
    dropanchorrecords = fields.One2many('vehicle_usage.vehicleanchor', 'vehicle_id', string=_('drop anchor record'))


class VehicleAnchor(models.Model):
    _name = 'vehicle_usage.vehicleanchor'

    # 关联的车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string=_('vehicle info'), required=True)
    # 内部编号
    inner_code = fields.Char(related='vehicle_id.inner_code', readonly=True)
    # 车牌号
    license_plate = fields.Char(related='vehicle_id.license_plate', readonly=True)
    # 车型
    model_id = fields.Many2one(related='vehicle_id.model_id', readonly=True)
    # 隶属公司
    company_id = fields.Many2one(related='vehicle_id.company_id', readonly=True)
    # 线路
    route_id = fields.Many2one(related='vehicle_id.route_id', readonly=True)
    # 抛锚时间
    anchortime = fields.Datetime(string=_('anchor time'))
    # 抛锚结束时间
    anchorend = fields.Datetime(string=_('anchor end time'))
    # 抛锚路段
    anchorroad = fields.Char(string=_('anchor road'))
    # 抛锚原因
    anchorreason = fields.Char(string=_('anchor reason'))
    # 解决方案
    solution = fields.Char(string=_('anchor solution'))
    # 抛锚时长
    anchorduration = fields.Char(compute='_computeAnchortime',string=_('anchor duration'))
    # 司机
    driver = fields.Many2one('hr.employee', string=_('driver'))

    @api.multi
    def _computeAnchortime(self):
        """
        计算抛锚时长
        """
        for item in self:
            try:
                start = time.mktime(time.strptime(item.anchortime, "%Y-%m-%d %H:%M:%S"))
                end = time.mktime(time.strptime(item.anchorend, "%Y-%m-%d %H:%M:%S"))
                if end <= start:
                    item.anchorduration = ''
                else:
                    hours = (end-start)/3600
                    item.anchorduration = '%.1f 小时' % hours
            except Exception:
                item.anchorduration = ''
