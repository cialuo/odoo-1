# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from itertools import izip_longest
import math
from utils import *

timeFormatStr = "%Y-%m-%d %H:%M:%S"

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
        mode = self.env['opertation_resources_station_platform']
        sitelist = mode.search([('route_id', '=', self.id), ('direction', '=', 'up')], order="sequence")
        sitecollection = []
        for item in sitelist:
            sitecollection.append((0, 0, {
                'site_id': item.station_id.id,
            }))

        # 下行大站检查
        mode = self.env['opertation_resources_station_platform']
        sitelist = mode.search([('route_id', '=', self.id), ('direction', '=', 'down')], order="sequence")
        sitecollection_down = []
        for item in sitelist:
            sitecollection_down.append((0, 0, {
                'site_id': item.station_id.id,
                'site_seq': item.sequence
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

class BusMoveExcuteTable(models.Model):
    """
    行车作业执行表
    """
    _name = "scheduleplan.excutetable"

    # 同一条线路同一天只有一个行车作业执行表
    _sql_constraints = [
        ('line_date_unique', 'unique (line_id, excutedate)', 'one line one date one execute table')
    ]

    name = fields.Char(string="excute table name")

    # 线路
    line_id = fields.Many2one("route_manage.route_manage", string="related line")

    # 行车规则id
    rule_id = fields.Many2one("scheduleplan.schedulrule", string="rule id")

    # 状态
    status = fields.Selection([("draft", "draft"),              # 草稿
                                ("wait4use", "wait for use"),   # 待使用
                                ("done", "done"),               # 完成
                              ], default="wait4use",  string="status")

    # 行车时刻表
    movetimetable_id = fields.Many2one("scheduleplan.busmovetime", string="move time tale")

    # 人车配班表
    staffarrangetable_id = fields.Many2one("bus_staff_group", string="staff arrange table")

    # 执行时间
    excutedate = fields.Date(string="excute date")

    # 首班时间
    firstruntime = fields.Datetime(string="first run time")

    # 末班时间
    lastruntime = fields.Datetime(string="last run time")

    # 首班时间
    downfirstruntime = fields.Datetime(string="down first run time")

    # 末班时间
    downlastruntime = fields.Datetime(string="down last run time")

    # 司机数量
    drivernum = fields.Integer(string="driver number")

    # 乘务员数量
    stewardnum = fields.Integer(string="steward number")

    # 上行趟次
    upmovenum = fields.Integer(string="up move number")

    # 下行趟次
    downmovenum =  fields.Integer(string="down move number")

    @api.multi
    def _getTotalMoveNumber(self):
        for item in self:
            item.totalmovenum = item.upmovenum + item.downmovenum

    # 总趟次
    totalmovenum = fields.Integer(compute="_getTotalMoveNumber", string="total move number")

    # 运营车辆
    workvehiclenum = fields.Integer(string="total work vehicles")

    # 机动车辆
    backupvehiclenum = fields.Integer(string="back up vehicle num")

    # 上行排班计划
    upmoveplan = fields.One2many("scheduleplan.execupplanitem", "execplan_id", string="up move plan")

    # 下行排班计划
    downmoveplan = fields.One2many("scheduleplan.execdownplanitem", "execplan_id", string="down move plan")

    # 出勤司乘
    motorcyclistsTime = fields.One2many("scheduleplan.motorcyclists", 'execplan_id', string="motorcyclists list")

    # 车辆资源
    vehicleresource = fields.One2many("scheduleplan.vehicleresource", 'execplan_id', string="vehicle resource")

class ExecUpPlanItem(models.Model):
    """
    作业执行表 上行排班计划
    """
    _name = "scheduleplan.execupplanitem"

    execplan_id = fields.Many2one("scheduleplan.excutetable", ondelete="cascade")

    # 序号
    seq_id = fields.Integer(string="sequence id", readonly=True)

    vehicle_id = fields.Many2one("fleet.vehicle", readonly=True)

    # 司机
    driver = fields.Many2one("hr.employee", string="dirver", readonly=True)

    # 乘务员
    steward = fields.Many2one("hr.employee", string="steward", readonly=True)

    # 发车时间
    starttime = fields.Datetime(string="start move time", readonly=True)

    # 到达时间
    arrivetime = fields.Datetime(string="arrive time", readonly=True)

    # 时长 分钟记
    timelenght = fields.Integer(string="time length (min)", readonly=True)

    # 里程
    mileage = fields.Integer(string="mileage number", readonly=True)

    rule_lineid = fields.Integer(compute="_getRuleLineId")

    @api.multi
    def _getRuleLineId(self):
        for item in self:
            item.rule_lineid = item.execplan_id.line_id

    # 线路
    line_id = fields.Many2one("route_manage.route_manage", string="related line",
                              domain="['|',('id','=',rule_lineid),('main_line_id','=',rule_lineid)]")


class ExecDownPlanItem(models.Model):
    """
    作业执行表 下行排班计划
    """

    _name = "scheduleplan.execdownplanitem"

    _inherit = "scheduleplan.execupplanitem"


class MotorcyclistsTime(models.Model):

    """
    出勤司乘
    """

    _name = "scheduleplan.motorcyclists"

    execplan_id = fields.Many2one("scheduleplan.excutetable", ondelete="cascade")

    employee_id = fields.Many2one("hr.employee", string="emplyee id")

    # 日期
    worktime = fields.Date(string="work date")

    vehicle_id = fields.Many2one("fleet.vehicle")

    # 职务
    title = fields.Selection([("driver", "driver"),          # 司机
                                     ("steward", "steward"),        # 乘务员
                                    ],  string="work title")

    # 工号
    employee_sn = fields.Char(related="employee_id.jobnumber", string="employee sn number")

    # 上班时间
    checkintime = fields.Datetime(string="check in time")

    # 实际发车时间
    realworkstart = fields.Datetime(string="real work start time")

    # 实际收车时间
    realworkdone = fields.Datetime(string="real work done time")

    # 下班时间
    checkouttime = fields.Datetime(string="check out time")

    # 工作时长（小时）
    worktimelength = fields.Float(string="work time lenght(hour)")

    # 运营时长（小时）
    workrealtimelength = fields.Float(string="work real time length(hour)")


class VehicleResource(models.Model):

    """
    车辆资源
    """

    _name = "scheduleplan.vehicleresource"

    execplan_id = fields.Many2one("scheduleplan.excutetable", ondelete="cascade")

    vehicle_id = fields.Many2one("fleet.vehicle")

    # 首班发车时间
    firstmovetime = fields.Datetime(string="first move time")

    # 末班发车时间
    lastmovetime = fields.Datetime(string="last move time")

    # 运营时长
    worktimelength = fields.Float(string="work time length")

    # 车辆台次
    arrangenumber = fields.Integer(string="arrange number")

    # 车辆状态
    workstatus = fields.Selection([('operation', "operation"),('flexible', "flexible")],
                                  default='operation', required=True)
