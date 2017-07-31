# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BusGroup(models.Model):
    """
    班组管理
    """
    _name = 'bus_group'

    name = fields.Char('Group Name', required=True)

    route_id = fields.Many2one('route_manage.route_manage')
    algorithm_id = fields.Many2one('bus_algorithm')
    shift_id = fields.Many2one('bus_shift')
    is_conductor = fields.Boolean(default=True)

    vehicle_ct = fields.Integer()
    driver_ct = fields.Integer()
    conductor_ct = fields.Integer()

    vehicle_ids = fields.One2many('bus_group_vehicle', 'bus_group_id')
    driver_ids = fields.One2many('bus_group_driver', 'bus_group_id')
    conductor_ids = fields.One2many('bus_group_conductor', 'bus_group_id')


class BusGroupVehicle(models.Model):
    """
    班组车辆
    """
    _name = 'bus_group_vehicle'

    bus_group_id = fields.Many2one('bus_group')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True,
                                domain = "[('vehicle_life_state', '=', 'operation_period')]")
    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id',
                                   readonly=True, copy=False)

    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id',
                                   readonly=True, copy=False)

    ride_number = fields.Integer('Ride Number', related='vehicle_id.ride_number', readonly=True)

    state = fields.Selection(related='vehicle_id.state')


class BusGroupDriver(models.Model):
    """
    班组司机
    """
    _name = 'bus_group_driver'

    bus_group_id = fields.Many2one('bus_group')

    driver_id = fields.Many2one('hr.employee', string="driver")
    jobnumber = fields.Char(string='employee work number', related='driver_id.jobnumber')


class BusGroupConductor(models.Model):
    """
    班组乘务员
    """
    _name = 'bus_group_conductor'

    bus_group_id = fields.Many2one('bus_group')
    conductor_id = fields.Many2one('hr.employee', string="conductor")
    jobnumber = fields.Char(string='employee work number', related='conductor_id.jobnumber')


