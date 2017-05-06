# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# 区域管理
class region_manage(models.Model):
    _name = 'region_manage.region_manage'

    _rec_name = 'region_name'

    # 区域编码 区域名称 设立时间 建档人 状态
    region_coding = fields.Char(_('Region coding'), required=True)
    region_name = fields.Char(_('Region name'), required=True)
    create_time = fields.Datetime(_('Creation time'))
    book_runner = fields.Many2one('res.users', string=_('Book runner'), default=lambda self: self.env.user)
    # road_id = fields.One2many('road_manage.road_manage', 'region_id', ondelete='cascade', string="Road")
    road_id = fields.One2many('road_manage.road_manage', 'region_id', ondelete='cascade', string=_("Road"))

    WORKFLOW_STATE_SELECTION = [
        ('inuse', _('In-use')),
        ('archive', _('Archive'))
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,
                             default='inuse',
                             string=_('State'),
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
        ('name_unique', 'unique(region_name)', _('The region name must be unique!')),
        ('coding_unique', 'unique(region_coding)', _('The region coding must be unique!'))
    ]

# 道路管理
class road_manage(models.Model):
    _name = 'road_manage.road_manage'

    _rec_name = 'road_name'

    # 道路编码 道路名称 区域 区域编码 设立日期 设立人 状态
    road_coding = fields.Char(_('Road coding'), required=True)    # 道路编码
    road_name = fields.Char(_('Road name'), required=True)    # 道路名称
    create_date = fields.Date(_('Creation date'))   # 建立日期
    book_runner = fields.Many2one('res.users', string=_('Book runner'), default=lambda self: self.env.user)    # 建档人

    # platform_id = fields.Many2many("platform_manage.platform_manage", string="Station")
    platform_id = fields.One2many("platform_manage.platform_manage", 'Road_id', string=_("Station"))
    region_id = fields.Many2one('region_manage.region_manage', ondelete='cascade', string=_('Region'), required=True)
    WORKFLOW_STATE_SELECTION = [
        ('inuse', _('In-use')),
        ('archive', _('Archive'))
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,  # 状态
                             default='inuse',
                             string=_('State'),
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
        ('name_unique', 'unique(road_name)', _('The road name must be unique!')),
        ('coding_unique', 'unique(road_coding)', _('The road coding must be unique!'))
    ]

# 站台管理
class platform_manage(models.Model):
    _name = 'platform_manage.platform_manage'

    _rec_name = "platform"

    longitude = fields.Float(digits=(10, 6), string=_("longitude"))    # 经度
    latitude = fields.Float(digits=(10, 6), string=_("latitude"))    # 纬度
    platform_number = fields.Char(_('Platform number'), required=True)    # 站台编号
    platform = fields.Char(_('Platform'), required=True)    # 站台名称
    entrance_azimuth = fields.Char(_('Entrance azimuth'))    # 进站方位角
    entrance_longitude = fields.Float(digits=(10, 6), string=_('Entrance longitude'))    # 进站经度
    entrance_latitude = fields.Float(digits=(10, 6), string=_('Entrance latitude'))    # 进站纬度
    exit_azimuth = fields.Char(_('Exit azimuth'))    # 出站方位角
    exit_longitude = fields.Float(digits=(10, 6), string=_('Exit longitude'))    # 出站经度
    exit_latitude = fields.Float(digits=(10, 6), string=_('Exit latitude'))    # 出站纬度
    platform_status = fields.Char(_('Platform status'))    # 站台状况
    electronic_bus_board_number = fields.Char(_('electronic bus-board number'))    # 电子站牌编号

    Road_id = fields.Many2one('road_manage.road_manage', ondelete='cascade', string=_('Road'), required=True)

    # route_id = fields.One2many('route_manage.route_manage', 'route_id', string='Route')

    # platform_resource = fields.Many2one('route_manage.route_manage', string="Platform resource")

    route_id = fields.Many2many('route_manage.route_manage', string=_('Route'))

    WORKFLOW_STATE_SELECTION = [
        ('inuse', _('In-use')),
        ('archive', _('Archive'))
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,
                             default='inuse',
                             string=_('State'),
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
        ('platform_unique', 'unique(platform)', _('The platform must be unique!')),
        ('platform_number_unique', 'unique(platform_number)', _('The platform number must be unique!'))
    ]

# 线路管理
class route_manage(models.Model):
    _name = 'route_manage.route_manage'
    _rec_name = 'route'

    route = fields.Char(_('Route'), required=True)  # 线路名称
    route_coding = fields.Char(_('Route NO.'), required=True)  # 线路编码
    route_type = fields.Selection([('single circle', _('Single circle')),  # 线路类型
                                   ('double circle', _('Double circle'))],
                                  default='double circle')

    first_half_class = fields.Selection([('up line', _('Up line')),    # 首趟半班
                                         ('down line', _('Down line'))], default="up line")

    oil_wear_coefficient = fields.Float(digits=(10, 2), string=_('Oil wear coefficient'))  # 油耗系数

    class_system = fields.Selection([('one-shift', _('One-shift')),    # 班制
                                     ('two-shift', _('Two-shift')),
                                     ('three-shift', _('Three-shift'))],
                                    default='one-shift')

    shunt_mode = fields.Selection([('single shunt', _('Single shunt')),    # 调车方式
                                   ('double shunt', _('Double shunt'))], default='single shunt')

    schedule_type = fields.Selection([('flexible scheduling', _('Flexible scheduling')),   # 调度方式
                                      ('planning scheduling', _('Planning scheduling')),
                                      ('hybrid scheduling', _('Hybrid scheduling'))],
                                     default='flexible scheduling')

    subsidiary = fields.Char(_('Subsidiary'))  # 隶属公司

    WORKFLOW_STATE_SELECTION = [
            ('inuse', _('In-use')),
            ('archive', _('Archive'))
        ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,
                             default='inuse',
                             string=_('State'),
                             readonly=True)

    # route_id = fields.Many2one('platform_manage.platform_manage', string='Route id')
    # platform_resource = fields.One2many('platform_manage.platform_manage', 'platform_resource', string='Platform')
    platform_resource = fields.Many2many('platform_manage.platform_manage', string=_('Platform'))
    human_resource = fields.Many2many('hr.employee', string=_('Human resource'))

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
        ('coding_unique', 'unique(route_coding)', _('The route coding must be unique!')),
        ('route_unique', 'unique(route)', _('The route name must be unique!')),
    ]

# 人力资源
class human_resource(models.Model):
    _inherit = 'hr.employee'

    # human_resource = fields.Many2one('route_manage.route_manage', string='Human resource')
    lines = fields.Many2many('route_manage.route_manage', string=_('Lines'))

