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

    # vehicle_ids = fields.One2many('fleet.vehicle', 'vehicle_id')



