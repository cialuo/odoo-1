# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re


class Area(models.Model):
    """
    区域管理
    """
    _name = 'opertation_resources_area'

    _sql_constraints = [
        ('name_unique', 'unique(name)', _('The area name must be unique!')),
        ('code_unique', 'unique(code)', _('The area code must be unique!'))
    ]

    name = fields.Char('Area name', required=True)  # 区域名称
    code = fields.Char('Area code', required=True) # 区域编码
    road_ids = fields.One2many('opertation_resources_road', 'area_id', ondelete='cascade', string="Road lists") # 所辖道路

    state = fields.Selection([('inuse', 'In-use'),('archive', 'Archive')],
                             default='inuse', string='area_state', readonly=True)  # 状态
    active = fields.Boolean(default=True)

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        self.active = True
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        self.active = False
        return True


class Road(models.Model):
    """
    道路管理
    """
    _name = 'opertation_resources_road'

    name = fields.Char('Road name', required=True)  # 道路名称
    code = fields.Char('Road code', required=True) # 道路编码
    area_id = fields.Many2one('opertation_resources_area', ondelete='cascade', string='Area', required=True) # 区域
    station_ids = fields.One2many("opertation_resources_station", 'road_id', string="Station lists")
    state = fields.Selection([('inuse', 'In-use'),('archive', 'Archive')],
                             default='inuse', string='road_state', readonly=True)  # 状态
    active = fields.Boolean(default=True)

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        self.active = True
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        self.active = False
        return True

    # sql 约束，效率高
    _sql_constraints = [
        ('name_unique', 'unique(name)', _('The road name must be unique!')),
        ('code_unique', 'unique(code)', _('The road code must be unique!'))
    ]


class Station(models.Model):
    _name = 'opertation_resources_station'

    _sql_constraints = [
        ('name_unique', 'unique(name)', _('The station name must be unique!')),
        ('code_unique', 'unique(code)', _('The station code must be unique!'))
    ]

    """
    站台管理
    """
    name = fields.Char('Station Name', required=True) # 站台名称
    code = fields.Char('Station Code', required=True) # 站台编号
    road_id = fields.Many2one('opertation_resources_road', ondelete='cascade', string='Road Choose', required=True)

    longitude = fields.Float(digits=(10, 6), string="longitude")  # 经度
    latitude = fields.Float(digits=(10, 6), string="latitude") # 纬度

    entrance_azimuth = fields.Integer('Entrance azimuth') # 进站方位角
    entrance_longitude = fields.Float(digits=(10, 6), string='Entrance longitude') # 进站经度
    entrance_latitude = fields.Float(digits=(10, 6), string='Entrance latitude') # 进站纬度

    exit_azimuth = fields.Integer('Exit azimuth') # 出站方位角
    exit_longitude = fields.Float(digits=(10, 6), string='Exit longitude') # 出站经度
    exit_latitude = fields.Float(digits=(10, 6), string='Exit latitude') # 出站纬度

    station_condition = fields.Char('Station Condition') # 站台状况
    electronic_bus_board_number = fields.Char('electronic bus-board number') # 电子站牌编号
    state = fields.Selection([('inuse', 'In-use'),('archive', 'Archive')],
                             default='inuse', string='station_state', readonly=True)  # 状态
    active = fields.Boolean(default=True)

    route_ids = fields.Many2many('route_manage.route_manage', 'opertation_resources_station_rel',
                                 'station_id', 'route_station_id', 'Station Routes')

    address = fields.Char()
    nearby = fields.Char()

    @api.multi
    def name_get(self):
        return [(i.id, '%s/%s' % (i.name, i.code)) for i in self]

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        self.active = True
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        self.active = False
        return True



class route_manage(models.Model):
    _name = 'route_manage.route_manage'
    """
    线路管理
    """

    @api.multi
    def _people_number(self):
        for item in self:
            item.people_number = len(item.human_resource)

    # 显示名称
    _rec_name = 'line_name'

    # sql 约束，效率高
    _sql_constraints = [
        # ('coding_unique', 'unique(gprs_id)', _('The route code must be unique!')),
        ('route_unique', 'unique(line_name)', _('The route name must be unique!')),
    ]

    line_name = fields.Char('Line Name', required=True) # 线路名称
    gprs_id = fields.Integer('gprsid', required=True) # 线路编码
    oil_wear_coefficient = fields.Float(digits=(10, 2), string='Oil wear coefficient') # 油耗系数
    class_system_name = fields.Selection([('one_shift', 'one_shift'),
                                        ('two_shift', 'two_shift'),
                                        ('three_shift', 'three_shift')],
                                        default='one_shift', required=True) # 班制
    run_type_name = fields.Selection([('single_shunt', 'single_shunt'),
                                   ('double_shunt', 'double_shunt')],
                                   default='double_shunt', required=True) # 调车方式
    schedule_type = fields.Selection([('flexible_scheduling', 'flexible_scheduling'),
                                      ('planning_scheduling', 'planning_scheduling'),
                                      ('hybrid_scheduling', 'hybrid_scheduling')],
                                      default='flexible_scheduling', required=True) # 调度方式

    department_id = fields.Many2one('hr.department', 'departmentName', required=True) # 隶属公司
    state = fields.Selection([('inuse', 'In-use'),('archive', 'Archive')],
                             default='inuse', string='Route State', readonly=True)  # 状态
    human_resource = fields.Many2many('hr.employee', string='Human resource') # 人力资源
    people_number = fields.Integer('People number', compute="_people_number")  # 人员数量
    active = fields.Boolean(default=True)
    line_type_name = fields.Selection([('main_line', 'main_line'),
                                    ('regional_line', 'regional_line'),
                                    ('express_line', 'express_line'),
                                    ('interval_line', 'interval_line')],
                                    default='main_line', required=True, string="Line Type")  # 线路类型

    main_line_id = fields.Many2one('route_manage.route_manage', string='Main Route',
                                    domain="[('line_type_name', '=', 'main_line')]") # 主线
    bus_type = fields.Selection([('regular_bus', 'regular_bus'),
                                 ('custom_bus', 'custom_bus')],
                                default='regular_bus', string='bus_type', required=True)  # 公交类型

    # station_up_ids = fields.One2many('opertation_resources_station_up', 'route_id', string='StationUps')
    # station_down_ids = fields.One2many('opertation_resources_station_down', 'route_id', string='StationDowns')

    station_up_ids = fields.One2many('opertation_resources_station_platform', 'route_id', string='StationUps',
                                     domain=[('direction', '=', 'up')])
    station_down_ids = fields.One2many('opertation_resources_station_platform', 'route_id', string='StationDowns',
                                     domain=[('direction', '=', 'down')])

    up_first_time = fields.Char('up_first_time', required=True, default='06:00') # 上行首班时间
    up_end_time = fields.Char('up_end_time', required=True, default='22:00')  # 上行首班时间
    down_first_time = fields.Char('down_first_time', required=True, default='06:30')  # 下行首班时间
    down_end_time = fields.Char('down_end_time', required=True, default='22:30')  # 下行首班时间
    up_station = fields.Many2one('opertation_resources_station', ondelete='cascade',
                                 compute='_get_station_up_first')  # 上行车场
    down_station = fields.Many2one('opertation_resources_station', ondelete='cascade',
                                   compute='_get_station_down_first')  # 下行车场
    mileage = fields.Float(digits=(10, 2), required=True)  #里程
    speed = fields.Float("Speed(km/h)", digits=(10, 2))  #速度

    station_route_ids = fields.Many2many('opertation_resources_station', 'opertation_resources_station_rel',
                                        'route_station_id', 'station_id', 'Stations')

    child_route_ids = fields.One2many('route_manage.route_manage', 'main_line_id', string='ChildRoutes')

    yard_ids = fields.One2many('opertation_resources_vehicle_yard', 'route_id', string='VehicleYards')

    start_date = fields.Datetime(string="Open date") #线路开始日期
    end_date = fields.Datetime(string="Stop date")  #线路停运日期
    is_artificial_ticket = fields.Boolean(default=True) #是否人工售票
    ticket_price = fields.Float() #票价

    loop_type = fields.Selection([('not_loop', 'not_loop'),
                                    ('single_loop', 'single_loop'),
                                    ('double_loop', 'double_loop'),
                                    ('double_line', 'double_line')],
                                    default='double_line', required=True)  # 线路类型

    @api.onchange('up_first_time','up_end_time','down_first_time','down_end_time')
    def _on_change_time(self):
        reg = '^(0\d{1}|1\d{1}|2[0-3]):([0-5]\d{1})$'
        if self.up_first_time:
            if not re.match(reg, self.up_first_time):
                self.up_first_time = ''
                return {
                    'warning': {
                        'title': _("Time format is not correct"),
                        'message': _("up_first_time not be Incorrect"),
                    },
                }

        if self.up_end_time:
            if not re.match(reg , self.up_end_time):
                self.up_end_time = ''
                return {
                    'warning': {
                        'title': _("Time format is not correct"),
                        'message': _("up_end_time not be Incorrect"),
                    },
                }
        if self.down_first_time:
            if not re.match(reg, self.down_first_time):
                self.down_first_time = ''
                return {
                    'warning': {
                        'title': _("Time format is not correct"),
                        'message': _("down_first_time not be Incorrect"),
                    },
                }

        if self.down_end_time:
            if not re.match(reg, self.down_end_time):
                self.down_end_time = ''
                return {
                    'warning': {
                        'title': _("Time format is not correct"),
                        'message': _("down_end_time not be Incorrect"),
                    },
                }


    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        self.active = True
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        self.active = False
        return True

    @api.model
    def create(self, vals):
        """
        """
        res = super(route_manage, self).create(vals)
        up_ids = res.station_up_ids.mapped('station_id')
        down_ids = res.station_down_ids.mapped('station_id')
        res_ids = up_ids | down_ids
        res.write({'station_route_ids': [(6, 0, res_ids.ids)]})
        return res

    @api.multi
    def write(self, vals):
        res = super(route_manage, self).write(vals)
        if vals.get('station_up_ids') or vals.get('station_down_ids'):
            up_ids = self.station_up_ids.mapped('station_id')
            down_ids = self.station_down_ids.mapped('station_id')
            res_ids = up_ids | down_ids
            vals= {'station_route_ids': [(6, 0, res_ids.ids)]}
            res = super(route_manage, self).write(vals)
        return res

    @api.depends('station_up_ids')
    def _get_station_up_first(self):
        for i in self:
            ups = i.station_up_ids.filtered(lambda field: field.sequence == 1)
            if ups:
                i.up_station = ups[0].station_id

    @api.depends('station_down_ids')
    def _get_station_down_first(self):
        for i in self:
            downs= i.station_down_ids.filtered(lambda field: field.sequence == 1)
            if downs:
                i.down_station = downs[0].station_id


class StationUp(models.Model):
    _name = 'opertation_resources_station_up'
    _rec_name = 'route_id'
    """
    上行站台管理
    """
    _sql_constraints = [
        ('sequence_unique', 'unique(sequence, route_id)', _('The up sequence and route must be unique!'))
    ]  # 站序，线路， 必须唯一

    sequence = fields.Integer("Station Sequence", default=2, required=True)
    route_id = fields.Many2one('route_manage.route_manage', ondelete='cascade', string='Route Choose', required=True)
    gprs_id = fields.Integer('code', related='route_id.gprs_id', required=True)  # 线路编码
    station_id = fields.Many2one('opertation_resources_station', ondelete='cascade', string='Station Choose',
                                 required=True)
    entrance_azimuth = fields.Integer('Entrance azimuth', related='station_id.entrance_azimuth', readonly=True) # 进站方位角
    entrance_longitude = fields.Float(digits=(10, 6), string='Entrance longitude',
                                      related='station_id.entrance_longitude', readonly=True) # 进站经度
    entrance_latitude = fields.Float(digits=(10, 6), string='Entrance latitude',
                                     related='station_id.entrance_latitude', readonly=True) # 进站纬度
    exit_azimuth = fields.Integer('Exit azimuth', related='station_id.exit_azimuth', readonly=True) # 出站方位角
    exit_longitude = fields.Float(digits=(10, 6), string='Exit longitude', related='station_id.exit_longitude',
                                  readonly=True) # 出站经度
    exit_latitude = fields.Float(digits=(10, 6), string='Exit latitude', related='station_id.exit_latitude',
                                 readonly=True) # 出站纬度
    station_type = fields.Selection([('first_station', 'first_station'),
                                     ('mid_station', 'mid_station'),
                                     ('last_station', 'last_station')], default='mid_station')

    is_show_name = fields.Boolean(default=True)

    @api.onchange('sequence')
    def _get_station_type(self):
        for i in self:
            if i.sequence == 1:
                i.station_type = 'first_station'


class StationDown(models.Model):
    _name = 'opertation_resources_station_down'
    _rec_name = 'route_id'
    """
    下行站台管理
    """
    _sql_constraints = [
        ('record_unique', 'unique(sequence,route_id)', _('The down sequence and route must be unique!'))
    ]  # 站序，线路， 必须唯一

    sequence = fields.Integer("Station Sequence", default=2, required=True)
    route_id = fields.Many2one('route_manage.route_manage', ondelete='cascade', string='Route Choose', required=True)
    gprs_id = fields.Integer('code', related='route_id.gprs_id', required=True)  # 线路编码
    station_id = fields.Many2one('opertation_resources_station', ondelete='cascade', string='Station Choose',
                                 required=True)
    entrance_azimuth = fields.Integer('Entrance azimuth', related='station_id.entrance_azimuth', readonly=True) # 进站方位角
    entrance_longitude = fields.Float(digits=(10, 6), string='Entrance longitude',
                                      related='station_id.entrance_longitude', readonly=True) # 进站经度
    entrance_latitude = fields.Float(digits=(10, 6), string='Entrance latitude',
                                     related='station_id.entrance_latitude', readonly=True) # 进站纬度
    exit_azimuth = fields.Integer('Exit azimuth', related='station_id.exit_azimuth', readonly=True) # 出站方位角
    exit_longitude = fields.Float(digits=(10, 6), string='Exit longitude', related='station_id.exit_longitude',
                                  readonly=True) # 出站经度
    exit_latitude = fields.Float(digits=(10, 6), string='Exit latitude', related='station_id.exit_latitude',
                                 readonly=True) # 出站纬度

    station_type = fields.Selection([('first_station', 'first_station'),
                                     ('mid_station', 'mid_station'),
                                     ('last_station', 'last_station')], default='mid_station', required=True)
    is_show_name = fields.Boolean(default=True)

    @api.onchange('sequence')
    def _get_station_type(self):
        for i in self:
            if i.sequence == 1:
                i.station_type = 'first_station'


# 人力资源
class human_resource(models.Model):
    _inherit = 'hr.employee'

    # human_resource = fields.Many2one('route_manage.route_manage', string='Human resource')
    # 所属线路
    lines = fields.Many2many('route_manage.route_manage', string='Choose Line')


class Platform(models.Model):
    _name = 'opertation_resources_station_platform'
    _rec_name = 'route_id'
    """
    站台管理
    """

    _sql_constraints = [
        ('sequence_unique', 'unique(sequence, route_id, direction)', _('The sequence and route must be unique!'))
    ] #站序，线路， 必须唯一

    direction = fields.Selection([('up', 'up'),
                                 ('down', 'down')], default='up')

    sequence = fields.Integer("Station Sequence", default=2, required=True)
    route_id = fields.Many2one('route_manage.route_manage', ondelete='cascade', string='Route Choose', required=True)
    gprs_id = fields.Integer('code', related='route_id.gprs_id', required=True)  # 线路编码
    station_id = fields.Many2one('opertation_resources_station', ondelete='cascade', string='Station Choose',
                                 required=True)
    entrance_azimuth = fields.Integer('Entrance azimuth', related='station_id.entrance_azimuth', readonly=True) # 进站方位角
    entrance_longitude = fields.Float(digits=(10, 6), string='Entrance longitude',
                                      related='station_id.entrance_longitude', readonly=True) # 进站经度
    entrance_latitude = fields.Float(digits=(10, 6), string='Entrance latitude',
                                     related='station_id.entrance_latitude', readonly=True) # 进站纬度
    exit_azimuth = fields.Integer('Exit azimuth', related='station_id.exit_azimuth', readonly=True) # 出站方位角
    exit_longitude = fields.Float(digits=(10, 6), string='Exit longitude', related='station_id.exit_longitude',
                                  readonly=True) # 出站经度
    exit_latitude = fields.Float(digits=(10, 6), string='Exit latitude', related='station_id.exit_latitude',
                                 readonly=True) # 出站纬度

    station_type = fields.Selection([('first_station', 'first_station'),
                                     ('mid_station', 'mid_station'),
                                     ('last_station', 'last_station')], default='mid_station', required=True)
    is_show_name = fields.Boolean(default=True)

    @api.onchange('sequence')
    def _get_station_type(self):
        for i in self:
            if i.sequence == 1:
                i.station_type = 'first_station'


class VehicleYard(models.Model):
    _name = 'opertation_resources_vehicle_yard'
    """
    车场
    """
    _sql_constraints = [
        ('code_unique', 'unique(code)', _('The yard code must be unique!'))
    ]
    name = fields.Char('Yard Name', required=True)
    code = fields.Integer("Yard Code", required=True)
    route_id = fields.Many2one('route_manage.route_manage', ondelete='cascade', string='Route Choose', required=True)
    direction = fields.Selection([('up', 'up'),
                                 ('down', 'down'),
                                ('one_way', 'one_way')], default='up')
    is_yard = fields.Boolean(default=True)

    dispatch_screen_ids = fields.One2many('opertation_resources_dispatch_screen', 'yard_id')


class DispatchScreen(models.Model):
    _name = 'opertation_resources_dispatch_screen'

    name = fields.Char('Screen Name', required=True)
    yard_id = fields.Many2one('opertation_resources_vehicle_yard')
    screen_code = fields.Char('Screen Code', required=True)
    screen_ip = fields.Char('Screen IP')
