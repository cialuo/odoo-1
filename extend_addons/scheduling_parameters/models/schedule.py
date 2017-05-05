# -*- coding: utf-8 -*-

from odoo import models, fields, api

# 区域管理
class region_manage(models.Model):
    _name = 'region_manage.region_manage'

    _rec_name = 'region_name'

    # 区域编码 区域名称 设立时间 建档人 状态
    region_coding = fields.Char('Region coding', required=True)
    region_name = fields.Char('Region name', required=True)
    create_time = fields.Datetime('Creation time')
    book_runner = fields.Many2one('res.users', string='Book runner')
    # road_id = fields.One2many('road_manage.road_manage', 'region_id', ondelete='cascade', string="Road")
    road_id = fields.One2many('road_manage.road_manage', 'region_id', ondelete='cascade', string="Road")

    WORKFLOW_STATE_SELECTION = [
        ('inuse', 'In-use'),
        ('archive', 'Archive')
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,
                             default='inuse',
                             string='State',
                             readonly=True)

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        return True

# 道路管理
class road_manage(models.Model):
    _name = 'road_manage.road_manage'

    _rec_name = 'road_name'

    # 道路编码 道路名称 区域 区域编码 设立日期 设立人 状态
    road_coding = fields.Char('Road coding', required=True)    # 道路编码
    road_name = fields.Char('Road name', required=True)    # 道路名称
    create_date = fields.Date('Creation date')   # 建立日期
    book_runner = fields.Many2one('res.users', string='Book runner')    # 建档人

    # platform_id = fields.Many2many("platform_manage.platform_manage", string="Station")
    platform_id = fields.One2many("platform_manage.platform_manage", 'Road_id', string="Station")
    region_id = fields.Many2one('region_manage.region_manage', ondelete='cascade', string='Region')
    WORKFLOW_STATE_SELECTION = [
        ('inuse', 'In-use'),
        ('archive', 'Archive')
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,  # 状态
                             default='inuse',
                             string='State',
                             readonly=True)

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        return True

# 站台管理
class platform_manage(models.Model):
    _name = 'platform_manage.platform_manage'

    _rec_name = "platform"

    longitude = fields.Float(digits=(10, 6), string="longitude")    # 经度
    latitude = fields.Float(digits=(10, 6), string="latitude")    # 纬度
    platform_number = fields.Char('Platform number', required=True)    # 站台编号
    platform = fields.Char('Platform', required=True)    # 站台名称
    entrance_azimuth = fields.Char('Entrance azimuth')    # 进站方位角
    entrance_longitude = fields.Float(digits=(10, 6), string='Entrance longitude')    # 进站经度
    entrance_latitude = fields.Float(digits=(10, 6), string='Entrance latitude')    # 进站纬度
    exit_azimuth = fields.Char('Exit azimuth')    # 出站方位角
    exit_longitude = fields.Float(digits=(10, 6), string='Exit longitude')    # 出站经度
    exit_latitude = fields.Float(digits=(10, 6), string='Exit latitude')    # 出站纬度
    platform_status = fields.Char('Platform status')    # 站台状况
    electronic_bus_board_number = fields.Char('electronic bus-board number')    # 电子站牌编号

    Road_id = fields.Many2one('road_manage.road_manage', ondelete='cascade', string='Road')

    # route_id = fields.One2many('route_manage.route_manage', 'route_id', string='Route')

    # platform_resource = fields.Many2one('route_manage.route_manage', string="Platform resource")

    route_id = fields.Many2many('route_manage.route_manage', string='Route')

    WORKFLOW_STATE_SELECTION = [
        ('inuse', 'In-use'),
        ('archive', 'Archive')
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,
                             default='inuse',
                             string='State',
                             readonly=True)

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        return True

# 线路管理
class route_manage(models.Model):
    _name = 'route_manage.route_manage'
    _rec_name = 'route'

    route = fields.Char('Route', required=True)  # 线路名称
    routeNO = fields.Char('Route NO.', required=True)  # 线路编码
    route_type = fields.Selection([('single circle', 'Single circle'),  # 线路类型
                                   ('double circle', 'Double circle')],
                                  default='double circle')

    first_half_class = fields.Selection([('up line', 'Up line'),    # 首趟半班
                                         ('down line', 'Down line')], default="up line")

    oil_wear_coefficient = fields.Float(digits=(10, 2), string='Oil wear coefficient')  # 油耗系数

    class_system = fields.Selection([('one-shift', 'One-shift'),    # 班制
                                     ('two-shift', 'Two-shift'),
                                     ('three-shift', 'Three-shift')],
                                    default='one-shift')

    shunt_mode = fields.Selection([('single shunt', 'Single shunt'),    # 调车方式
                                   ('double shunt', 'Double shunt')], default='single shunt')

    schedule_type = fields.Selection([('flexible scheduling', 'Flexible scheduling'),   # 调度方式
                                      ('planning scheduling', 'Planning scheduling'),
                                      ('hybrid scheduling', 'Hybrid scheduling')],
                                     default='flexible scheduling')

    subsidiary = fields.Char('Subsidiary')  # 隶属公司

    driver_per_vehicle = fields.Char('Driver per vehicle')
    steward_per_vehicle = fields.Char('Steward per vehicle')
    line_synthesis_person_per_vehicle = fields.Char('Line synthesis person per vehicle')

    WORKFLOW_STATE_SELECTION = [
            ('inuse', 'In-use'),
            ('archive', 'Archive')
        ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,
                             default='inuse',
                             string='State',
                             readonly=True)

    # route_id = fields.Many2one('platform_manage.platform_manage', string='Route id')
    # platform_resource = fields.One2many('platform_manage.platform_manage', 'platform_resource', string='Platform')
    platform_resource = fields.Many2many('platform_manage.platform_manage', string='Platform')
    human_resource = fields.Many2many('hr.employee', string='Human resource')

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        return True

# 人力资源
class human_resource(models.Model):
    _inherit = 'hr.employee'

    # human_resource = fields.Many2one('route_manage.route_manage', string='Human resource')
    lines = fields.Many2many('route_manage.route_manage', string='Lines')

