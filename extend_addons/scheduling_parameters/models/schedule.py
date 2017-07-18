# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Area(models.Model):
    """
    区域管理
    """
    _name = 'opertation_resources_area'

    name = fields.Char('Area name', required=True)  # 区域名称
    code = fields.Char('Area code', required=True) # 区域编码
    road_ids = fields.One2many('opertation_resources_road', 'area_id', ondelete='cascade', string="Road") # 所辖道路

    state = fields.Selection([('inuse', 'In-use'),('archive', 'Archive')],
                             default='inuse', string='State', readonly=True)  # 状态
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
        ('name_unique', 'unique(name)', _('The area name must be unique!')),
        ('code_unique', 'unique(code)', _('The area code must be unique!'))
    ]


class Road(models.Model):
    """
    道路管理
    """
    _name = 'opertation_resources_road'

    name = fields.Char('Road name', required=True)  # 道路名称
    code = fields.Char('Road code', required=True) # 道路编码
    area_id = fields.Many2one('opertation_resources_area', ondelete='cascade', string='Area', required=True) # 区域
    station_ids = fields.One2many("opertation_resources_station", 'road_id', string="Station")
    state = fields.Selection([('inuse', 'In-use'),('archive', 'Archive')],
                             default='inuse', string='State', readonly=True)  # 状态
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
    """
    站台管理
    """

    name = fields.Char('Station Name', required=True) # 站台名称
    code = fields.Char('Station Code', required=True) # 站台编号
    road_id = fields.Many2one('opertation_resources_road', ondelete='cascade', string='Road', required=True)

    longitude = fields.Float(digits=(10, 6), string="longitude")  # 经度
    latitude = fields.Float(digits=(10, 6), string="latitude") # 纬度

    entrance_azimuth = fields.Char('Entrance azimuth') # 进站方位角
    entrance_longitude = fields.Float(digits=(10, 6), string='Entrance longitude') # 进站经度
    entrance_latitude = fields.Float(digits=(10, 6), string='Entrance latitude') # 进站纬度

    exit_azimuth = fields.Char('Exit azimuth') # 出站方位角
    exit_longitude = fields.Float(digits=(10, 6), string='Exit longitude') # 出站经度
    exit_latitude = fields.Float(digits=(10, 6), string='Exit latitude') # 出站纬度

    station_status = fields.Char('Station status') # 站台状况
    electronic_bus_board_number = fields.Char('electronic bus-board number') # 电子站牌编号
    state = fields.Selection([('inuse', 'In-use'),('archive', 'Archive')],
                             default='inuse', string='State', readonly=True)  # 状态

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
        ('name_unique', 'unique(name)', _('The station name must be unique!')),
        ('code_unique', 'unique(code)', _('The station code must be unique!'))
    ]

# 线路管理
class route_manage(models.Model):
    _name = 'route_manage.route_manage'

    @api.multi
    def _people_number(self):
        for item in self:
            item.people_number = len(item.human_resource)

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
    subsidiary = fields.Many2one('hr.department', 'Subsidiary')


    state = fields.Selection([('inuse', 'In-use'),('archive', 'Archive')],
                             default='inuse', string='State', readonly=True)  # 状态


    # 站台资源
    platform_resource = fields.Many2many('opertation_resources_station', string='Platform')
    # 人力资源
    human_resource = fields.Many2many('hr.employee', string='Human resource')
    # 人员数量
    people_number = fields.Integer('People number', compute="_people_number")

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
        ('coding_unique', 'unique(route_coding)', _('The route coding must be unique!')),
        ('route_unique', 'unique(route)', _('The route name must be unique!')),
    ]

# 人力资源
class human_resource(models.Model):
    _inherit = 'hr.employee'

    # human_resource = fields.Many2one('route_manage.route_manage', string='Human resource')
    # 所属线路
    lines = fields.Many2many('route_manage.route_manage', string='Lines')

