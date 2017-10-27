# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions,_
import time,datetime
import odoo.addons.decimal_precision as dp

class usage_record(models.Model):

    _name = 'energy.usage_record'
    _inherit = ['mail.thread']
    _description = 'Energy usage record'
    _rec_name = 'vehicle_id'

    """
       使用记录
    """

    #能源站
    station_id = fields.Many2one('energy.station',string='Station Id',required=True)

    #能源桩
    pile_id = fields.Many2one('energy.pile',string='Pile Id',domain="[('station_id', '=', station_id)]")

    #车辆
    vehicle_id = fields.Many2one('fleet.vehicle',string='Vehicle Id',required=True,domain="[('vehicle_life_state', '=', 'operation_period'),('state', '=', 'normal')]")

    #状态
    state = fields.Selection([('normal', 'Normal'), ('stop', 'Stop')],default='normal')

    def _default_utcnow(self):
        """
            获取当前UTC时间
        :return:
        """
        return datetime.datetime.utcnow()

    #使用能源时间
    record_date = fields.Datetime(string='Record Date',default=_default_utcnow)

    #加油人
    operator = fields.Many2one('hr.employee',string='Operator')

    #使用人:司机
    user_use = fields.Many2many('hr.employee',string='User Use')

    #能源型号
    energy_type = fields.Many2one('product.product',string='Energy Type',required=True,domain="[('important_type', '=', 'energy')]")

    #能源桩类型
    pile_type = fields.Selection(string='Pile Type', related='pile_id.pile_type', store=True,)

    #车牌号
    license_plate = fields.Char(string='License Plate',related='vehicle_id.license_plate', store=False,readonly=True)

    #车辆编号
    inner_code = fields.Char(string='Inner Code',related='vehicle_id.inner_code', store=True,readonly=True)

    #使用量
    fuel_capacity = fields.Float(string='Fuel Capacity',required=True)

    #单位
    companyc_id = fields.Many2one(related='energy_type.uom_id',store=True,string='Companyc Id',readonly=True)

    #库位
    location_id = fields.Many2one('stock.location', related='pile_id.location_id', store=False, readonly=True,
                                  string='Location Id')

    #运营里程
    working_mileage = fields.Float(string='Working Mileage',readonly=True)

    #gps里程
    gps_mileage = fields.Float(string='GPS Mileage',readonly=True)

    #运营油耗
    working_oil_wear  = fields.Float(string='Working Oil Wear ')

    #gps油耗
    gps_oil_wear = fields.Float(string='GPS Oil Wear ')

    #库位单价
    location_price = fields.Float(string='Location Price',digits=(12,2))

    # 使用总价
    total_price = fields.Float(string='Total Price',digits=(12,2),readonly=True,compute='_compute_total_price')

    active = fields.Boolean(string="MyActive", default=True)


    @api.onchange('pile_id')
    def _onchange_pile_id(self):
        """
            能源桩变更修改能源信息
        :return:
        """
        if self.pile_id != None:
            self.energy_type = self.pile_id.energy_type

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id_driver(self):
        """
            车辆变更时,修改司机的数据
        :return:
        """
        if self.vehicle_id != None:
            self.user_use = self.vehicle_id.driver

    @api.onchange('energy_type')
    def _onchange_energy_type(self):
        """
            能源变更时修改单价
        :return:
        """
        if self.energy_type != None:
            self.location_price = self.energy_type.list_price

    @api.depends('location_price','fuel_capacity')
    def _compute_total_price(self):
        """
            根据使用量和单价计算总价：
                总价 = 单价 * 使用量
        :return:
        """
        self.total_price = self.location_price * self.fuel_capacity

    @api.multi
    def normal_to_stop(self):
        self.state = 'stop'
        self.active =False

    @api.multi
    def stop_to_normal(self):
        self.state = 'normal'
        self.active = True

    @api.model
    def create(self, vals):
        """
            复写模块的创建方法,在生成使用记录的同事,新增库位移动记录
        :param vals:
        :return:
        """
        vals = self._onchange_vehicle_id(vals)
        res = super(usage_record, self).create(vals)
        self._vehicle_move(vals)
        return res

    def _vehicle_move(self,vals):
        """
            创建一个库存移动
        :param vals:
        :return:
        """

        station = self.env['energy.station'].search([('id', '=', vals.get('station_id'))])

        if station.station_property == 'company':
            """
                公司内部的能源站
            """
            if vals.get('pile_id'):
                # 获取能源桩信息
                pile = self.env['energy.pile'].search([('id', '=', vals.get('pile_id'))])
                product_id = pile.energy_type
                location_id = pile.location_id.id
                picking_type_id = self.env.ref('energy_management.picking_energy_management_company').id
            else:
                raise exceptions.UserError(_("Companies to provide energy, the need to choose energy piles!"))
        else:
            """
                供应商的能源站
            """
            product_id = self.env['product.product'].search([('id', '=', vals.get('energy_type'))])
            location_id =self.env.ref('stock.stock_location_suppliers').id
            picking_type_id = self.env.ref('energy_management.picking_energy_management_supplier').id

        #获取车辆信息
        vehicle = self.env['fleet.vehicle'].search([('id', '=', vals.get('vehicle_id'))])

        move_vals = {
                'name': 'CN-' + product_id.display_name,
                'product_id': product_id.id,
                'product_uom_qty': vals.get('fuel_capacity'),
                'product_uom': product_id.uom_id.id,
                'location_id':location_id,
                'location_dest_id':vehicle.location_id.id,
                'picking_type_id':picking_type_id
        }
        moves = self.env['stock.move'].create(move_vals)
        moves.action_done()

    #@api.onchange('vehicle_id','fuel_capacity')
    def _onchange_vehicle_id(self,vals):
        """
            当车辆变更的时候,计算并修改车辆的运营里程、GPS里程、运营油耗、GPS油耗
        :return:
        """
        domain = [('vehicle_id', '=', vals.get('vehicle_id'))]

        #获取车辆的最后一次能源使用记录id
        usage_record = self.env['energy.usage_record'].search(domain,limit=1,order="record_date desc")

        if usage_record:
            domain += [('realityarrive', '>=', usage_record.record_date)]
            driverecords = self.env['vehicleusage.driverecords'].search(domain)
        else:
            driverecords = self.env['vehicleusage.driverecords'].search(domain)

        #叠加运营里程和GPS里程
        working_mileage = 0
        gps_mileage = 0
        for driverecord in driverecords:
            working_mileage += driverecord.planmileage
            gps_mileage += driverecord.GPSmileage

        #计算油耗
        if usage_record and working_mileage >0 and gps_mileage > 0:
            """
                上次加油量/当前里程 * 100
            """
            vals['working_oil_wear'] = usage_record.fuel_capacity / working_mileage * 100
            vals['gps_oil_wear'] = usage_record.fuel_capacity / gps_mileage * 100

        vals['working_mileage'] = working_mileage
        vals['gps_mileage'] = gps_mileage


        return vals



class vehicle_usage_record(models.Model):

    _inherit = ['fleet.vehicle']

    """
        继承车辆信息,新增能源记录
    """

    @api.depends('average_day_number')
    def _compute_average_oil_wear(self):
        """
            根据天数计算百里油耗
        :return:
        """

        today = datetime.datetime.now()

        for i in self:

            yesterday = today - datetime.timedelta(days=i.average_day_number)


            domain = ['&',('vehicle_id', '=', i.id),('create_date', '>=', yesterday)]

            records = self.env['energy.usage_record'].search(domain)

            # 叠加运营里程和GPS里程
            working_mileage = 0
            working_oil_wear = 0
            for record in records:
                working_mileage += record.working_mileage
                working_oil_wear += record.fuel_capacity

            # 计算油耗
            if working_mileage > 0:
                """
                        总加油量 / 总里程 * 100
                """
                i.average_oil_wear = round(working_oil_wear / working_mileage,4) * 100


    #能源记录
    energy_usage_record_ids = fields.One2many('energy.usage_record','vehicle_id',string='energy_usage_record_ids')

    #平均百里油耗
    average_oil_wear = fields.Float(string='Average Oil Wear',compute=_compute_average_oil_wear,digits=dp.get_precision('Operate pram'))

    #company_id = fields.Many2one('res.company', 'Company',
                                 #default=lambda self: self.env['res.company']._company_default_get(
                                     #'fleet.vehicle'),
                                 #index=True, required=True)
    # 平均油耗天数
    #average_day_number = fields.Integer(related='company_id.average_day_number', default=30)

    #average_day_number = fields.Integer(string='Average Day Number',default=30)

    @api.multi
    def action_to_usage_record(self):
        """
            跳转到能源使用记录
        :return:
        """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('energy_management', xml_id)
            res.update(
                context=dict(self.env.context),
                domain=[('vehicle_id', '=', self.id)]
            )
            return res
        return False

class fleet_vehicle_model(models.Model):

    _inherit = 'fleet.vehicle.model'

    """
        继承车型，在车型里新增平均油耗,并计算值
    """

    @api.multi
    def _compute_model_average_oil_wear(self):

        """
            默认计算值:
            1.获取车型下的所有所有车辆信息
            2.获取每一辆的平均百里油耗
            3.(车辆1的百里油耗 + ... 车辆N的百里油耗) / 车辆数 = 车型平均油耗
        :return:
        """
        for model in self:
            vehicles = self.env['fleet.vehicle'].search([('model_id','=',model.id)])
            if len(vehicles) > 0:
                model.model_average_oil_wear = sum(vehicles.mapped('average_oil_wear')) / len(vehicles)

    model_average_oil_wear = fields.Float(string='Average Oil Wear', compute=_compute_model_average_oil_wear,digits=(12,2))

