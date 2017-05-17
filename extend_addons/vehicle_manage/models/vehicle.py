# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime


class Vehicle(models.Model):
    """
    车辆档案
    """
    _inherit = "fleet.vehicle"
    _sql_constraints = [('code_uniq', 'unique (inner_code)', _("inner code already exists")),
                        ('license_plate_uniq', 'unique(license_plate)', _('The license_plate must be unique !')),]

    state = fields.Selection([('warrantly', "warrantly"),
                              ('normal', "normal"),
                              ('rush', "rush"),
                              ('repair', "repair"),
                              ('stop', "stop"),], default='normal',
                               help='Current state of the vehicle', ondelete="set null")
    name = fields.Char("Vehicle Number", compute="_cumpute_model_name", store=True)
    inner_code = fields.Char(string="Inner Code", help="Inner Code", required=True)
    route_id = fields.Many2one('route_manage.route_manage', string="Route")
    company_id = fields.Many2one('hr.department', 'Company')

    engine_no = fields.Char("Engine No",related='model_id.engine_no')
    transmission_ext = fields.Char(related='model_id.transmission_ext', store=True, readonly=True, copy=False)
    fuel_type_ext = fields.Char(related='model_id.fuel_type_ext', store=True, readonly=True, copy=False)
    co2_ext = fields.Float(related='model_id.co2_ext', store=True, readonly=True, copy=False)
    horsepower_ext = fields.Integer(related='model_id.horsepower_ext', store=True, readonly=True, copy=False)
    power_ext = fields.Integer(related='model_id.power_ext', store=True, readonly=True, copy=False)

    weight = fields.Integer(related='model_id.weight', store=True, readonly=True, copy=False)
    doors_ext = fields.Integer(related='model_id.doors_ext', store=True, readonly=True, copy=False)
    seats_ext = fields.Integer(related='model_id.seats_ext', store=True, readonly=True, copy=False)

    brand_name = fields.Char(compute="_compute_model_att_name", store=True)
    length_width_height = fields.Char(compute="_compute_model_att_name", help='length_width_height')

    reg_no = fields.Char(help='The registration number')
    reg_date = fields.Date(help='Reg Date')
    forced_destroy = fields.Char(help='Forced to destroy')
    annual_inspection_date = fields.Date(help='The annual inspection date', required=True)
    emissions = fields.Char(help='The vehicle emissions')
    total_odometer = fields.Float(compute='_get_total_odometer', string='Total Odometer', help='Total Odometer')

    vehicle_label = fields.Selection([('yellow', "Yellow"),
                              ('green', "Green")], default='green',
                               help='Vehicle Label')

    deadline = fields.Integer(string="Deadline",related='model_id.deadline') #使用寿命


    emission_standard = fields.Many2one(related='model_id.emission_standard')

    location_id = fields.Many2one('stock.location', string='V Location')
    location_stock_id = fields.Many2one('stock.location', string='Stock Location')

    start_service_date = fields.Date(string='Start Service Date')   #投入日期
    # service_float_year = fields.Float('Service Float Year', compute='_get_service_year')
    service_year = fields.Integer('Service Year', compute='_get_salvage_rate')

    salvage_rate = fields.Float(string='Salvage Rate', compute='_get_salvage_rate')  # 年限残值

    # 售票员
    conductor = fields.Many2many('hr.employee', relation='vehicle_conductor_employee', string="conductor")
    # 司机
    driver = fields.Many2many('hr.employee', relation='vehicle_driver_employee', string="driver")

    route_correct_value = fields.Float(related='route_id.oil_wear_coefficient', string="oil_wear_coefficient")

    @api.depends('start_service_date')
    def _get_salvage_rate(self):
        for i in self:
            if not i.start_service_date:
                continue
            start = fields.Datetime.from_string(i.start_service_date)
            today = datetime.today()
            i.salvage_rate = (today-start).days/365.0/(i.deadline or 15)
            i.service_year = int((today - start).days / 365.0+1)

    @api.model
    def create(self, vals):
        """
        创建车辆时，同时为车辆创建两个库位-- 虚拟库位/（车牌号）， 库存/（车牌号）
        :param vals:
        :return:
        """
        res = super(Vehicle, self).create(vals)
        name = res.license_plate
        virtual_parent = self.env.ref('stock.stock_location_locations_virtual', raise_if_not_found=False)
        stock_vals = self.env['stock.location'].create({
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'name': name,
            'usage': 'internal',
            'is_vehicle': True,
        })
        virtual_vals = self.env['stock.location'].create({
            'location_id': virtual_parent.id,
            'name': name,
            'usage': 'inventory',
            'is_vehicle': True,
        })
        res.write({'location_id': virtual_vals.id, 'location_stock_id': stock_vals.id})
        return res


    @api.depends('inner_code')
    def _cumpute_model_name(self):
        for record in self:
            record.name = record.inner_code

    @api.depends('model_id')
    def _compute_model_att_name(self):
        for record in self:
            record.brand_name = record.model_id.brand_id.name
            record.length_width_height = str(record.model_id.length)+'*'+str(record.model_id.width)+'*'+str(record.model_id.height)

    def _get_total_odometer(self):
        """
        获取车辆累计的行程公里数
        """
        for record in self:
            vehicle_odometer = self.env['fleet.vehicle.odometer'].search([('vehicle_id', '=', record.id)])
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

    transmission_ext = fields.Char('Transmission', help='Transmission')
    fuel_type_ext = fields.Char('Fuel Type', help='Fuel Type')
    co2_ext = fields.Float('CO2 Emissions', help='CO2 emissions of the vehicle')
    horsepower_ext = fields.Integer("Horsepower")
    power_ext = fields.Integer('Power', help='Power in KW of the vehicle')
    weight = fields.Integer('Weight', help='Weight')
    doors_ext = fields.Integer('Doors Number', help='Number of doors of the vehicle')
    seats_ext = fields.Integer('Seats Number', help='Number of seats of the vehicle', default=5)

    home_entry_date = fields.Date("Home Entry Date", help='Home Entry Date')
    specifications = fields.Char("Specifications", help='Specifications')
    engine_no = fields.Char("Engine No")
    chassis_no = fields.Char('Chassis No')
    length = fields.Integer("Length", help='Length')
    width = fields.Integer("Width", help='Width')
    height = fields.Integer("Height", help='Height')
    inner_height = fields.Integer('Inner Height', help='Inner Height')

    front_distance = fields.Integer('Front Distance', help='Front Distance')
    rear_distance = fields.Integer('Rear Distance', help='Rear Distance')
    shaft_distance = fields.Integer('Shaft Distance', help='Shaft Distance')
    front_max_weight = fields.Integer('Front Max Weight', help='Front Max Weight')
    rear_max_weight = fields.Integer('Rear Max Weight', help='Rear Max Weight')
    wheel_count = fields.Integer('Wheel Count',help='Wheel Count')
    driving_wheel_count = fields.Integer('Driving Wheel Count', help='Driving Wheel Count')
    turn_radius = fields.Float('Turn Radius',help='Turn Radius')
    max_climb = fields.Integer('Max Climb',help='Max Climb')
    fuel_capacity = fields.Float('Fuel Capacity',help='Fuel Capacity')
    fuel_consumption_pre_hund = fields.Float(help='Every hundred kilometers rated fuel consumption')
    deadline = fields.Integer(string="Deadline", default=15)
    manufacturers = fields.Char(help='Manufacturers')
    note = fields.Text("Note", help='Note')

    emission_standard = fields.Many2one('vehicle_manage.emission_standard', 'Emission Standard')


class VehicleEmissionStandard(models.Model):
    """
    排放标准
    """
    _name = 'vehicle_manage.emission_standard'
    _sql_constraints = [('stand_code_unique', 'unique(level_code)', _('Standard code already exists'))]

    name = fields.Char("Emission Level", help="Emission Level", required=True)
    remark = fields.Text("Remark", help="Remark")
    level_code = fields.Char('Level Code', help='Level Code', required=True)


# 线路管理
class route_manage(models.Model):
    _inherit = 'route_manage.route_manage'

    # 车辆资源
    vehicle_res = fields.One2many('fleet.vehicle', 'route_id', string="vehicle resource")

    # 驾驶员比例
    driver_rate = fields.Float(compute='_getDriverRate' ,string="driver rate")

    # 车辆数量
    vehiclenums = fields.Integer("vehicle number", compute='_getVehicleNums')

    @api.multi
    def _getVehicleNums(self):
        for item in self:
            item.vehiclenums = self.getVehicleNumber(item.id)

    # 获取线路驾驶员数量
    def getDriverNumber(self, routeid):
        hrmode = self.env['hr.employee']
        return hrmode.search_count([('lines', '=', routeid),('workpost.posttype', '=', 'driver')])

    # 获取售票员数量
    def getConductorNumber(self, routeid):
        hrmode = self.env['hr.employee']
        return hrmode.search_count([('lines', '=', routeid),('workpost.posttype', '=', 'conductor')])

    # 获取车辆数量
    def getVehicleNumber(self, routeid):
        vehiclemode = self.env['fleet.vehicle']
        return vehiclemode.search_count([('route_id', '=', routeid)])

    @api.multi
    def _getDriverRate(self):
        for item in self:
            # vehiclenum = self.getVehicleNumber(item.id)
            vehiclenum = item.vehiclenums
            drivernum = self.getDriverNumber(item.id)
            if vehiclenum != 0:
                item.driver_rate = round(drivernum/vehiclenum,1)
            else:
                item.driver_rate = 0

    # 售票员比例
    conductor_rate = fields.Float(compute='_getConductorRate',string="conductor rate")

    @api.multi
    def _getConductorRate(self):
        for item in self:
            vehiclenum = item.vehiclenums
            conductornum = self.getConductorNumber(item.id)
            if vehiclenum != 0 :
                item.conductor_rate = round(conductornum/vehiclenum, 1)
            else:
                item.conductor_rate = 0

    # 综合比例
    synthesize_rate = fields.Float(compute='_getSynthesizeRate' ,string="synthesize rate")

    @api.multi
    def _getSynthesizeRate(self):
        for item in self:
            vehiclenum = self.getVehicleNumber(item.id)
            all = item.people_number
            if vehiclenum != 0:
                item.synthesize_rate = round(all/vehiclenum, 1)
            else:
                item.synthesize_rate = 0


