# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BusStaffGroup(models.Model):
    """
    人车配班
    """
    _name = 'bus_staff_group'
    name = fields.Char()
    route_id = fields.Many2one('route_manage.route_manage', required=True)
    bus_algorithm_id = fields.Many2one('bus_algorithm', required=True)
    bus_driver_algorithm_id = fields.Many2one('bus_driver_algorithm', required=True)

    group_line_ids = fields.One2many('bus_staff_group_line', 'staff_group_id')


class BusStaffGroupLine(models.Model):
    """
    人车配班详情
    """
    _name = 'bus_staff_group_line'
    _rec_name = 'vehicle_id'

    staff_group_id = fields.Many2one('bus_staff_group')

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True)
    state = fields.Selection(related='vehicle_id.state', readonly=True)

    operation_state = fields.Selection([('operation', "operation"),('flexible', "flexible")], default='operation',
                                        required=True)

