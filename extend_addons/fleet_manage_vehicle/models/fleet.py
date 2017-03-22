# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FleetVehicle(models.Model):
    """
    车辆档案
    """
    _inherit = "fleet.vehicle"

    state = fields.Selection([('warrantly', "warrantly"),
                              ('normal', "normal"),
                              ('rush', "rush"),
                              ('repair', "repair"),
                              ('stop', "stop"),], default='normal',
                               help='Current state of the vehicle', ondelete="set null")
    inner_code = fields.Char(string="Inner Code",help="Inner Code")
    route_id = fields.Many2one('fleet_manage_vehicle.route',string="Route")
    trainman = fields.Many2one('hr.employee', string="Trainman Name")
    driver = fields.Many2one('hr.employee', string="Driver Name", required=True)
    engine_no = fields.Char('Engine No',help='Engine No')
    transmission_ext = fields.Char(related='model_id.transmission_ext', store=True, readonly=True, copy=False)
    fuel_type_ext = fields.Char(related='model_id.fuel_type_ext', store=True, readonly=True, copy=False)
    co2_ext = fields.Float(related='model_id.co2_ext', store=True, readonly=True, copy=False)
    horsepower_ext = fields.Integer(related='model_id.horsepower_ext', store=True, readonly=True, copy=False)
    power_ext = fields.Integer(related='model_id.power_ext', store=True, readonly=True, copy=False)

    weight = fields.Integer(related='model_id.weight', store=True, readonly=True, copy=False)
    doors_ext = fields.Integer(related='model_id.doors_ext', store=True, readonly=True, copy=False)
    seats_ext = fields.Integer(related='model_id.seats_ext', store=True, readonly=True, copy=False)

    brand_name = fields.Char(compute="_compute_model_att_name", store=True)
    length_width_height = fields.Char(compute="_compute_model_att_name",help='length_width_height')

    reg_no = fields.Char(help='The registration number')
    reg_date = fields.Date(help='Reg Date')
    forced_destroy = fields.Char(help='Forced to destroy')
    annual_inspection_date = fields.Date(help='The annual inspection date')
    emissions = fields.Char(help='The vehicle emissions')
    total_odometer = fields.Float(compute='_get_total_odometer', string='Total Odometer', help='Total Odometer')

    @api.depends('model_id')
    def _compute_model_att_name(self):
        for record in self:
            record.brand_name = record.model_id.brand_id.name
            record.length_width_height = str(record.model_id.length)+'*'+str(record.model_id.width)+'*'+str(record.model_id.height)

    def _get_total_odometer(self):
        """
        获取车辆累计的行程公里数
        """
        FleetVehicalOdometer = self.env['fleet.vehicle.odometer']
        for record in self:
            vehicle_odometer = FleetVehicalOdometer.search([('vehicle_id', '=', record.id)])
            if vehicle_odometer:
                record.total_odometer = sum(i.value for i in vehicle_odometer)
            else:
                record.total_odometer = 0


class FleetVehicleModel(models.Model):
    """
    车型管理
    """
    _inherit = 'fleet.vehicle.model'

    code = fields.Char(string="Code", help='Code')

    transmission_ext = fields.Char('Transmission',help='Transmission')
    fuel_type_ext = fields.Char('Fuel Type',help='Fuel Type')
    co2_ext = fields.Float('CO2 Emissions', help='CO2 emissions of the vehicle')
    horsepower_ext = fields.Integer("Horsepower")
    power_ext = fields.Integer('Power', help='Power in KW of the vehicle')
    weight = fields.Integer('Weight',help='Weight')
    doors_ext = fields.Integer('Doors Number', help='Number of doors of the vehicle', default=5)
    seats_ext = fields.Integer('Seats Number', help='Number of seats of the vehicle')


    reg_date = fields.Date("Reg Date",help='Reg Date')
    specifications = fields.Char("Specifications",help='Specifications')
    engine_type_no = fields.Char("Engine Type No",help='Engine Type No')
    chassis_no = fields.Integer('Chassis No',help='Chassis No')
    length = fields.Integer("Length",help='Length')
    width = fields.Integer("Width",help='Width')
    height = fields.Integer("Height",help='Height')
    inner_height = fields.Integer('Inner Height',help='Inner Height')

    front_distance = fields.Integer('Front Distance',help='Front Distance')
    rear_distance = fields.Integer('Rear Distance',help='Rear Distance')
    shaft_distance = fields.Integer('Shaft Distance',help='Shaft Distance')
    front_max_weight = fields.Integer('Front Max Weight',help='Front Max Weight')
    rear_max_weight = fields.Integer('Rear Max Weight',help='Rear Max Weight')
    wheel_count = fields.Integer('Wheel Count',help='Wheel Count')
    driving_wheel_count = fields.Integer('Driving Wheel Count',help='Driving Wheel Count')
    turn_radius = fields.Float('Turn Radius',help='Turn Radius')
    max_climb = fields.Integer('Max Climb',help='Max Climb')
    fuel_capacity = fields.Float('Fuel Capacity',help='Fuel Capacity')
    fuel_consumption_pre_hund = fields.Float(help='Every hundred kilometers rated fuel consumption')
    deadline = fields.Float(string="Deadline")
    manufacturers = fields.Char(help='Manufacturers')
    note = fields.Text("Note",help='Note')


class FleetVehicleRoute(models.Model):
    """
    车型管理
    """
    _name = 'fleet_manage_vehicle.route'

    name = fields.Char("Route Name", help='Route Name')