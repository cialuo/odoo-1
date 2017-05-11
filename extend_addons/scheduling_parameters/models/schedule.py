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
    book_runner = fields.Many2one('res.users', string='Book runner', default=lambda self: self.env.user)
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

    # sql 约束，效率高
    _sql_constraints = [
        ('name_unique', 'unique(region_name)', 'The region name must be unique!'),
        ('coding_unique', 'unique(region_coding)', 'The region coding must be unique!')
    ]

# 道路管理
class road_manage(models.Model):
    _name = 'road_manage.road_manage'

    _rec_name = 'road_name'

    # 道路编码 道路名称 区域 区域编码 设立日期 设立人 状态
    # 道路编码
    road_coding = fields.Char('Road coding', required=True)
    # 道路名称
    road_name = fields.Char('Road name', required=True)
    # 区域
    region_id = fields.Many2one('region_manage.region_manage', ondelete='cascade', string='Region', required=True)
    # 设立日期
    create_date = fields.Date('Create date')
    # 建档人
    book_runner = fields.Many2one('res.users', string='Book runner', default=lambda self: self.env.user)

    # platform_id = fields.Many2many("platform_manage.platform_manage", string="Station")
    platform_id = fields.One2many("platform_manage.platform_manage", 'Road_id', string="Station")
    # 状态
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

    # sql 约束，效率高
    _sql_constraints = [
        ('name_unique', 'unique(road_name)', 'The road name must be unique!'),
        ('coding_unique', 'unique(road_coding)', 'The road coding must be unique!')
    ]

# 站台管理
class platform_manage(models.Model):
    _name = 'platform_manage.platform_manage'

    _rec_name = "platform"
    # 经度
    longitude = fields.Float(digits=(10, 6), string="longitude")
    # 纬度
    latitude = fields.Float(digits=(10, 6), string="latitude")
    # 站台编号
    platform_number = fields.Char('Platform number', required=True)
    # 站台名称
    platform = fields.Char('Platform', required=True)
    # 进站方位角
    entrance_azimuth = fields.Char('Entrance azimuth')
    # 进站经度
    entrance_longitude = fields.Float(digits=(10, 6), string='Entrance longitude')
    # 进站纬度
    entrance_latitude = fields.Float(digits=(10, 6), string='Entrance latitude')
    # 出站方位角
    exit_azimuth = fields.Char('Exit azimuth')
    # 出站经度
    exit_longitude = fields.Float(digits=(10, 6), string='Exit longitude')
    # 出站纬度
    exit_latitude = fields.Float(digits=(10, 6), string='Exit latitude')
    # 站台状况
    platform_status = fields.Char('Platform status')
    # 电子站牌编号
    electronic_bus_board_number = fields.Char('electronic bus-board number')

    Road_id = fields.Many2one('road_manage.road_manage', ondelete='cascade', string='Road', required=True)

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

    # sql 约束，效率高
    _sql_constraints = [
        ('platform_unique', 'unique(platform)', 'The platform must be unique!'),
        ('platform_number_unique', 'unique(platform_number)', 'The platform number must be unique!')
    ]

# 线路管理
class route_manage(models.Model):
    _name = 'route_manage.route_manage'

    # 显示名称
    _rec_name = 'route'

    # 线路名称
    route = fields.Char('Route', required=True)
    # 线路编码
    route_coding = fields.Char('Route NO.', required=True)
    # 线路类型
    route_type = fields.Selection([('single circle', 'Single circle'),
                                   ('double circle', 'Double circle')],
                                  default='double circle')
    # 首趟半班
    first_half_class = fields.Selection([('up line', 'Up line'),
                                         ('down line', 'Down line')], default="up line")
    # 油耗系数
    oil_wear_coefficient = fields.Float(digits=(10, 2), string='Oil wear coefficient')

    # 班制
    class_system = fields.Selection([('one-shift', 'One-shift'),
                                     ('two-shift', 'Two-shift'),
                                     ('three-shift', 'Three-shift')],
                                    default='one-shift')
    # 调车方式
    shunt_mode = fields.Selection([('single shunt', 'Single shunt'),
                                   ('double shunt', 'Double shunt')], default='single shunt')
    # 调度方式
    schedule_type = fields.Selection([('flexible scheduling', 'Flexible scheduling'),
                                      ('planning scheduling', 'Planning scheduling'),
                                      ('hybrid scheduling', 'Hybrid scheduling')],
                                     default='flexible scheduling')
    # 隶属公司
    subsidiary = fields.Char('Subsidiary')

    # 状态
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
    # 站台资源
    platform_resource = fields.Many2many('platform_manage.platform_manage', string='Platform')
    # 人力资源
    human_resource = fields.Many2many('hr.employee', string='Human resource')

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        return True

    # sql 约束，效率高
    _sql_constraints = [
        ('coding_unique', 'unique(route_coding)', 'The route coding must be unique!'),
        ('route_unique', 'unique(route)', 'The route name must be unique!'),
    ]

# 人力资源
class human_resource(models.Model):
    _inherit = 'hr.employee'

    # human_resource = fields.Many2one('route_manage.route_manage', string='Human resource')
    # 所属线路
    lines = fields.Many2many('route_manage.route_manage', string='Lines')

