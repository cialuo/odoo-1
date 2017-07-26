# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime,timedelta
import odoo.addons.decimal_precision as dp


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

    license_plate = fields.Char(required=True, help='车牌')
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

    deadline = fields.Integer(string="Deadline",related='model_id.deadline', readonly=True) #使用寿命


    emission_standard = fields.Many2one(related='model_id.emission_standard', readonly=True)

    location_id = fields.Many2one('stock.location', string='V Location')
    location_stock_id = fields.Many2one('stock.location', string='Stock Location')

    start_service_date = fields.Date(string='Start Service Date')   #投入日期

    service_year = fields.Integer('Service Year', compute='_get_salvage_rate')

    salvage_rate = fields.Float(string='Salvage Rate', compute='_get_salvage_rate')  # 年限残值

    # 售票员
    conductor = fields.Many2many('hr.employee', relation='vehicle_conductor_employee', string="conductor")
    # 司机
    driver = fields.Many2many('hr.employee', relation='vehicle_driver_employee', string="driver")

    #线路修正系数
    route_correct_value = fields.Float(related='route_id.oil_wear_coefficient', string="oil_wear_coefficient", readonly=True)

    #2017年7月24日 ERP-394 新增字段：编码(车辆创建时，自动生成)
    vehicle_code = fields.Char(string='Vehicle Code',default='/',readonly=True)

    #2017年7月24日 ERP-431 新增字段：日均里程
    daily_mileage = fields.Float(string='Daily Mileage',readonly=True,digits=dp.get_precision('Operate pram'),compute='_compute_daily_mileage')

    company_id_s = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('fleet.vehicle'),
                                 index=True, required=True)

    average_day_number = fields.Integer(related='company_id_s.average_day_number', default=30)

    @api.depends('driverecords')
    def _compute_daily_mileage(self):
        """
            计算日均里程：
                周期总里程 / 周期天数 ， 周期天数 =  百公里油耗设置的周期
        :return:
        """
        today = datetime.now()

        for order in self:
            yesterday = today - timedelta(days=order.average_day_number)
            driverecords = order.driverecords.filtered(lambda x: x.realityarrive >= unicode(yesterday))
            if driverecords:
                order.daily_mileage = sum(driverecords.mapped('GPSmileage')) / order.average_day_number

    @api.multi
    def return_action_to_mileage(self):
        """
            刷新
        :return:
        """
        return False
    def get_vehicle_code(self,vals):
        """
            生成车辆编码：
                车型代码+车辆自编号+投入运营（年份2位数）

                初始车辆编码只有 车型代码 + 车辆自编号
                当车辆投入运营时，加上年份数
        :return:
        """
        vehicle_code = "/"
        vehicle_model = self.env['fleet.vehicle.model'].search([('id', '=', vals.get('model_id'))])

        self_number = vals.get('inner_code',"")
        vehicle_model_code = vehicle_model.code if vehicle_model.code else ""

        vehicle_code = vehicle_model_code + self_number

        return vehicle_code

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        lp_copied_count = self.search_count(
            [('license_plate', '=like', _(u"Copy of {}%").format(self.license_plate))])
        if not lp_copied_count:
            new_license_plate = _(u"Copy of {}").format(self.license_plate)
        else:
            new_license_plate = _(u"Copy of {} ({})").format(self.license_plate, lp_copied_count)

        default['license_plate'] = new_license_plate

        inc_copied_count = self.search_count(
            [('inner_code', '=like', _(u"Copy of {}%").format(self.inner_code))])
        if not inc_copied_count:
            new_inner_code = _(u"Copy of {}").format(self.inner_code)
        else:
            new_inner_code = _(u"Copy of {} ({})").format(self.inner_code, inc_copied_count)

        default['inner_code'] = new_inner_code

        return super(Vehicle, self).copy(default)

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
        vals['vehicle_code'] = self.get_vehicle_code(vals)
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
    seats_ext = fields.Integer('Seats Number', help='Number of seats of the vehicle')

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


class InheritVehicle(models.Model):

    _inherit = "fleet.vehicle"

    """
        新增车辆录入流
    """

    entry_state = fields.Selection([('draft','draft'),('submitted','submitted'),('audited','audited')],string='Entry state',default='draft')

    def draft_to_submitted(self):
        """
            状态：草稿--->已提交
        :return:
        """
        self.entry_state = 'submitted'

    def submitted_to_audited(self):
        """
            状态：已提交--->已审核
        :return:
        """
        self.entry_state = 'audited'

    def submitted_to_draft(self):
        """
            状态：已提交--->草稿
        :return:
        """
        self.entry_state = 'draft'