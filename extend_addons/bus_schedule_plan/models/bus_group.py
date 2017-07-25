# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class BusGroup(models.Model):
    """
    班组管理
    """
    _name = 'bus_group'

    name = fields.Char('Group Name', required=True)
    route_id = fields.Many2one('route_manage.route_manage', required=True)
    is_conductor = fields.Boolean(default=True)

    vehicle_ct = fields.Integer(compute='get_vehicle_ct')
    driver_ct = fields.Integer(compute='get_driver_ct')
    conductor_ct = fields.Integer(compute='get_conductor_ct')

    vehicle_ids = fields.One2many('bus_group_vehicle', 'bus_group_id')
    driver_ids = fields.One2many('bus_group_driver', 'bus_group_id')
    conductor_ids = fields.One2many('bus_group_conductor', 'bus_group_id')

    @api.depends('vehicle_ids')
    def get_vehicle_ct(self):
        for i in self:
            i.vehicle_ct = len(i.vehicle_ids)

    @api.depends('driver_ids')
    def get_driver_ct(self):
        for i in self:
            i.driver_ct = len(i.driver_ids)

    @api.depends('conductor_ids')
    def get_conductor_ct(self):
        for i in self:
            i.conductor_ct = len(i.conductor_ids)

    @api.onchange('route_id')
    def _get_route_id_onchange(self):
        for i in self:
            datas = []
            for j in i.route_id.vehicle_res.ids:  #更新车辆
                res = self.env['bus_group'].search([('route_id', '=', i.route_id.id)])
                lists = []
                for k in res:
                    if k.name == self.name:
                        continue
                    lists += k.vehicle_ids.mapped('vehicle_id').ids
                if j in lists:
                    continue
                vals = {
                    "route_id": i.route_id.id,
                    'vehicle_id': j,
                }
                datas.append((0, 0, vals))
            i.vehicle_ids = datas

            datas = []
            for j in i.route_id.human_resource.filtered(lambda field: field.workpost.posttype == "driver").ids: #更新司机
                res = self.env['bus_group'].search([('route_id', '=', i.route_id.id)])
                lists = []
                for k in res:
                    if k.name == self.name:
                        continue
                    lists += k.driver_ids.mapped('driver_id').ids
                if j in lists:
                    continue
                vals = {
                    "route_id": i.route_id.id,
                    'driver_id': j,
                }
                datas.append((0, 0, vals))
            i.driver_ids = datas

            datas = []
            for j in i.route_id.human_resource.filtered(lambda field: field.workpost.posttype == "conductor").ids: #更新乘务员
                res = self.env['bus_group'].search([('route_id', '=', i.route_id.id)])
                lists = []
                for k in res:
                    if k.name == self.name:
                        continue
                    lists += k.conductor_ids.mapped('conductor_id').ids
                if j in lists:
                    continue
                vals = {
                    "route_id": i.route_id.id,
                    'conductor_id': j,
                }
                datas.append((0, 0, vals))
            i.conductor_ids = datas


class BusGroupVehicle(models.Model):
    """
    班组车辆
    """
    _name = 'bus_group_vehicle'
    _rec_name = 'vehicle_id'

    _sql_constraints = [
        ('record_unique', 'unique(route_id,vehicle_id)', _('The route and vehicle must be unique!'))
    ]

    bus_group_id = fields.Many2one('bus_group')
    route_id = fields.Many2one('route_manage.route_manage')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True,
                                 domain="[('route_id','=',route_id)]")
    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id',
                                   readonly=True, copy=False)
    ride_number = fields.Integer('Ride Number', related='vehicle_id.ride_number', readonly=True)
    state = fields.Selection(related='vehicle_id.state', readonly=True, string="Vehicle State")


class BusGroupDriver(models.Model):
    """
    班组司机
    """
    _name = 'bus_group_driver'
    _rec_name = 'driver_id'

    route_id = fields.Many2one('route_manage.route_manage', readonly=True)
    bus_group_id = fields.Many2one('bus_group')
    driver_id = fields.Many2one('hr.employee', string="driver", required=True,
                                domain="[('workpost.posttype', '=', 'driver')]")
    jobnumber = fields.Char(string='employee work number', related='driver_id.jobnumber', readonly=True)


class BusGroupConductor(models.Model):
    """
    班组乘务员
    """
    _name = 'bus_group_conductor'
    _rec_name = 'conductor_id'

    bus_group_id = fields.Many2one('bus_group')
    conductor_id = fields.Many2one('hr.employee', string="conductor", required=True,
                                   domain="[('workpost.posttype', '=', 'conductor')]")
    jobnumber = fields.Char(string='employee work number', related='conductor_id.jobnumber', readonly=True)


