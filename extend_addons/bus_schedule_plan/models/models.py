# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RouteInBusSchedule(models.Model):

    _inherit = "route_manage.route_manage"

    @api.multi
    def outputRule(self):
        """
        输出规则
        """
        type = self._context.get('bustype', False)
        self.ensure_one()

        # 上行大站检查
        mode = self.env['opertation_resources_station_up']
        sitelist = mode.search([('route_id', '=', self.id)])
        sitecollection = []
        for item in sitelist:
            sitecollection.append((0, 0, {
                'site_id': item.id,
            }))

        # 下行大站检查
        mode = self.env['opertation_resources_station_down']
        sitelist = mode.search([('route_id', '=', self.id)])
        sitecollection_down = []
        for item in sitelist:
            sitecollection_down.append((0, 0, {
                'site_id': item.id,
            }))

        context = dict(self.env.context,
                       default_line_id=self.id,
                       default_mileage=self.mileage,
                       default_bus_number =self.vehiclenums,
                       default_upfirsttime=self.up_first_time,
                       default_uplasttime=self.up_end_time,
                       default_downfirsttime = self.down_first_time,
                       default_downlasttime = self.down_end_time,
                       default_upstation = self.up_station.id,
                       default_downstation = self.down_station.id,
                       default_bustype = type,
                       default_bigsite_up = sitecollection,
                       default_bigsite_down = sitecollection_down,
                       default_bus_type = self.bus_type,
                       )
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'scheduleplan.schedulrule',
            'type': 'ir.actions.act_window',
            'res_id': '',
            'context': context
        }

class BusWorkRules(models.Model):

    _name = 'scheduleplan.schedulrule'

    name = fields.Char(string="rule name")

    line_id = fields.Many2one("route_manage.route_manage", string="related line", readonly=True)

    def _defaultType(self):
        type = self._context.get('bustype', False)
        if type == 'normal':
            return 'normal'
        elif type == 'custem':
            return 'custem'

    # 公交类型
    bustype = fields.Selection([("normal", "normal bus"),           # 普通公交
                                ("custem", "custem bus"),           # 定制公交
                              ], default=_defaultType,  string="bus type", readonly=True)

    # 调车方式
    schedule_method = fields.Selection([("singleway", "single way"),        # 单头调
                                        ("dubleway", "dubleway"),           # 双头调
                                        ], default="singleway", string="schedule method", required=True)

    # 线路里程
    mileage = fields.Float(string="line mile age", readonly=True)

    # 可用车数
    bus_number = fields.Integer(string="bus number", readonly=True)

    # 上行首班时间
    upfirsttime = fields.Char(string="up first time", readonly=True)

    # 上行末班时间
    uplasttime = fields.Char(string="up last time", readonly=True)

    # 下行首班时间
    downfirsttime = fields.Char(string="down first time", readonly=True)

    # 下行末班时间
    downlasttime = fields.Char(string="down last time", readonly=True)

    # 上行车场
    upstation = fields.Many2one("opertation_resources_station", string="up station", readonly=True)

    # 下行车场
    downstation = fields.Many2one("opertation_resources_station", string="down station", readonly=True)

    # 自动生成时刻表
    autogen = fields.Boolean(string="auto generate times")

    # 上行配车方案
    upplanvehiclearrange = fields.One2many("scheduleplan.up.rulebusarrange", "rule_id",
                                           string="up plan vehicle arrange")

    # 上行发车方案
    uptimearrange = fields.One2many("scheduleplan.toup", "rule_id", string="up time arrange")

    # 下行配车方案
    downplanvehiclearrange = fields.One2many("scheduleplan.down.rulebusarrange", "rule_id",
                                             string="up plan vehicle arrange")

    # 下行发车方案
    downtimearrange = fields.One2many("scheduleplan.todown", "rule_id", string="up time arrange")

    # 大站设置 上行
    bigsite_up = fields.One2many("scheduleplan.bigsitesetup", "rule_id", string="big site up")


    # 大站设置 下行
    bigsite_down = fields.One2many("scheduleplan.bigsitesetdown", "rule_id",string="big site down")

    # 公交类型
    bus_type = fields.Selection([('regular_bus', 'regular_bus'),
                                 ('custom_bus', 'custom_bus')],
                                default='regular_bus', string='bus_type', required=True)

    @staticmethod
    def _validateVehicleNums(obj):
        vcount = 0
        for item in obj.upplanvehiclearrange:
            vcount += item.allvehicles

        for item in obj.downplanvehiclearrange:
            vcount += item.allvehicles

        if vcount > obj.bus_number:
            raise ValidationError(_("vechile count large then vehicle number"))


    @staticmethod
    def _validate_sqenum(datalist):
        """
        验证序号为单调递增 且增量为1
        """
        for i in range(1, len(datalist)):
            if (datalist[i] - datalist[i-1]) != 1:
                raise ValidationError(_("difference bettwen two sequence number must be 1"))

    @staticmethod
    def _validate_startendtime(datalist, start, end):
        if datalist[0].starttime != start or datalist[-1].endtime != end:
            raise ValidationError(_("start and end time not match"))

    @staticmethod
    def _validateTimeContinuity(datalist):
        """
        验证排班时间的连续性
        """
        for i in range(1, len(datalist)):
            if datalist[i].starttime != datalist[i-1].endtime:
                raise ValidationError(_("time arrange must have continuity"))


    @staticmethod
    def _validate(dataList, startTime, endTime, type):
        newlist = sorted(dataList, key=lambda k: k.seqid)
        BusWorkRules._validate_sqenum(newlist)
        BusWorkRules._validate_startendtime(newlist, startTime, endTime)
        BusWorkRules._validateTimeContinuity(newlist)

    @staticmethod
    def _validate_scheduleplan(obj):
        """
        验证发车规则是否正确
        """
        if obj.schedule_method == "singleway":
            BusWorkRules._validate(obj.uptimearrange, obj.upfirsttime, obj.uplasttime, "singleway")
        elif obj.schedule_method == "dubleway":
            BusWorkRules._validate(obj.uptimearrange, obj.upfirsttime, obj.uplasttime, "dubleway")
            BusWorkRules._validate(obj.downtimearrange, obj.downfirsttime, obj.downlasttime, "dubleway")


    @api.model
    def create(self, vals):
        res = super(BusWorkRules, self).create(vals)
        self._validateVehicleNums(res)
        self._validate_scheduleplan(res)
        return res

    @api.multi
    def write(self, vals):
        res = super(BusWorkRules, self).write(vals)
        self._validateVehicleNums(self)
        self._validate_scheduleplan(self)
        return res

    def createMoveTimeTable(self):
        """
        生成行车时刻表
        """
        pass


class RuleBusArrangeUp(models.Model):

    """
    配车方案 上行
    """

    _name = "scheduleplan.up.rulebusarrange"


    rule_id = fields.Many2one("scheduleplan.schedulrule", string="related rule")

    # 车型
    vehiclemode = fields.Many2one("fleet.vehicle.model", string="vehicle mode")

    # 运营数量
    workingnumber = fields.Integer(string="vehicle working number")

    # 机动车数量
    backupnumber = fields.Integer(string="vehicle backup number")

    # 核载人数
    passengernumber = fields.Integer(related="vehiclemode.ride_number", string="passenger number")

    # 车辆总数
    allvehicles = fields.Integer(compute="_sumvehicles", string="all vehcile number")

    @api.depends('workingnumber', 'backupnumber')
    def _sumvehicles(self):
        self.allvehicles = self.workingnumber + self.backupnumber


class ToUp(models.Model):
    """
    上行发车安排
    """
    _name = "scheduleplan.toup"

    rule_id = fields.Many2one("scheduleplan.schedulrule", string="related rule")

    # 开始时间
    starttime = fields.Char(string="start time", required=True)

    # 发车次序id
    seqid = fields.Integer(string="sequence id", required=True)

    # 结束时间
    endtime = fields.Char(string="end time", required=True)

    # 间隔
    interval = fields.Integer(string="interval", required=True)

    # 车速
    speed = fields.Float(string="vehicle speed")

    # 运营时长
    worktimelength = fields.Integer(string="line work time length")

    # 停车时间
    resttime = fields.Integer(string="rest time")

    # 最小配车数
    minvehicles = fields.Integer(string="min vehicle number")

    # 满载率
    rateoffullload = fields.Float(string="rate of full load")

    # 标志
    mark = fields.Selection([("peak", "peak"),        # 高峰
                            ("flat", "flat"),         # 平峰
                            ("low", "low"),           # 低峰
                            ], string="load mark")

    # 跨天
    spanday = fields.Boolean(string="span day")

    @api.one
    @api.constrains('interval')
    def _check_interval(self):
        if self.interval <= 0:
            raise ValidationError(_("interval must be an positive integer"))


class RuleBusArrangeDown(models.Model):

    """
    下行配车方案
    """
    _name = "scheduleplan.down.rulebusarrange"

    _inherit = "scheduleplan.up.rulebusarrange"


class ToDown(models.Model):
    """
    下行发车安排
    """
    _name = "scheduleplan.todown"

    _inherit = "scheduleplan.toup"


class BigSiteSettingsUp(models.Model):

    _name = "scheduleplan.bigsitesetup"

    rule_id = fields.Many2one("scheduleplan.schedulrule", string="related rule")

    site_id = fields.Many2one("opertation_resources_station_up")

    # 是否签点
    needsign = fields.Boolean(string="need sign")

    # 是否大站考核
    needchecking = fields.Boolean(string="need checking")

    # 距上一站时间(低峰)
    tolastsit_low = fields.Integer(string="to last site time (low)")

    # 距上一站时间(平峰)
    tolastsit_flat = fields.Integer(string="to last site time (flat)")

    # 距上一站时间(高峰)
    tolastsit_peak = fields.Integer(string="to last site time (high)")

    # 允许快几分钟
    fastthen = fields.Integer(string="fast allowed")

    # 允许慢几分钟
    slowthen = fields.Integer(string="slow allowed")


class BigSiteSettingsDown(models.Model):

    _name = "scheduleplan.bigsitesetdown"

    _inherit = "scheduleplan.bigsitesetup"

    site_id = fields.Many2one("opertation_resources_station_down")



class BusMoveTimeTable(models.Model):

    """
    行车时刻表
    """

    _name = "scheduleplan.busmovetime"

    name = fields.Char(string="table name")

    # 关联线路
    line_id = fields.Many2one("route_manage.route_manage", string="related line", readonly=True)

    # 关联规则
    rule_id = fields.Many2one("scheduleplan.schedulrule", string="related rule")

    # 运营车辆
    vehiclenums = fields.Integer(string="vehicle nums")

    # 机动车辆
    backupvehicles = fields.Integer(string="backup vehicles")

    # 执行时间
    executedate = fields.Date(string="excute date")

    # 调车方式
    schedule_method = fields.Selection([("singleway", "single way"),  # 单头调
                                        ("dubleway", "dubleway"),  # 双头调
                                        ], default="singleway", string="schedule method", required=True)

    # 计划趟次
    plan_totaltimes = fields.Integer(string="plan total times")

    # 实际趟次
    real_times = fields.Integer(string="real total times")

    # 上行发车时间安排
    uptimeslist = fields.One2many("scheduleplan.movetimeup", "movetimetable_id", string="up times arrange")

    # 下行发车时间安排
    downtimeslist = fields.One2many("scheduleplan.movetimedown", "movetimetable_id", string="down times arrange")

class MoveTimeUP(models.Model):

    _name = "scheduleplan.movetimeup"

    movetimetable_id = fields.Many2one("scheduleplan.busmovetime")

    # 序号
    seqid = fields.Integer(string="sequence id")

    # 发车时间
    startmovetime = fields.Datetime(string="start move time")

    # 到达时间
    arrive_time = fields.Datetime(string="arrive time")

    # 时长
    timelength = fields.Integer(string="move time length")

    # 里程
    mileage = fields.Integer(string="move mile age")

    # 线路
    line_id = fields.Many2one("route_manage.route_manage", string="related line")

    # 起始站点
    start_site = fields.Many2one("opertation_resources_station", string="start site")

    # 结束站点
    end_site = fields.Many2one("opertation_resources_station", string="end site")


class MoveTimeDown(models.Model):

    _name = "scheduleplan.movetimedown"

    _inherit = "scheduleplan.movetimeup"


class BusMoveExcuteTable(models.Model):

    _name = "scheduleplan.excutetable"

    name = fields.Char(string="excute table name")



    