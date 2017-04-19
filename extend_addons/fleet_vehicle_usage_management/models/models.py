# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time

# class fleet_vehicle_usage_management(models.Model):
#     _name = 'fleet_vehicle_usage_management.fleet_vehicle_usage_management'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class FleetVehicle(models.Model):
    """
    车辆档案
    """
    _inherit = "fleet.vehicle"

    warnning = fields.Boolean(compute="_needwarnning")

    def _needwarnning(self):
        for item in self:
            d = item.annual_inspection_date
            if d != False:
                timeArray = time.strptime(d, "%Y-%m-%d")
                timeStamp = int(time.mktime(timeArray))
                currenttime = int(time.time())
                if ( currenttime + 15552000 )> timeStamp :
                    item.warnning = True
                else:
                    item.warnning = False
            else:
                item.warnning = False


