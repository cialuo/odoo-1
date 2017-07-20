# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BusWorkRules(models.Model):

    _name = 'scheduleplan.schedulrule'

    name = fields.Char(string="rule name")

    line_id = fields.Many2one("route_manage.route_manage", string="related line")

    # 公交类型
    bustype = fields.Selection([("normal", "normal bus"),           # 普通公交
                                ("custem", "custem bus"),           # 定制公交
                              ],  string="bus type")

    # 调车方式
    schedule_method = fields.Selection([("singleway", "single way"),        # 单头调
                                        ("dubleway", "dubleway"),           # 双头调
                                        ], string="schedule method")

    # 线路里程
    mileage = fields.Float(string="line mile age", store=True)

    # 可用车数
    bus_number = fields.Integer(string="bus number", store=True)

    # 上行首班时间
    upfirsttime = fields.Char(string="up first time", store=True)

    # 上行末班时间
    uplasttime = fields.Char(string="up last time", store=True)

    # 下行首班时间
    downfirsttime = fields.Char(string="down first time", store=True)

    # 下行末班时间
    downlasttime = fields.Char(string="down last time", store=True)

    # 上行车场
    upstation = fields.Char(string="up station")

    # 下行车场
    downstation = fields.Char(string="down station")

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
    bigsite_down = fields.One2many("scheduleplan.bigsitesetdown", "rule_id", string="big site down")


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

    #
    # passengernumber = fields.Integer(string="passenger number")


class ToUp(models.Model):
    """
    上行发车安排
    """
    _name = "scheduleplan.toup"

    rule_id = fields.Many2one("scheduleplan.schedulrule", string="related rule")

    # 开始时间
    starttime = fields.Char(string="start time")

    # 结束时间
    endtime = fields.Char(string="end time")

    # 间隔
    interval = fields.Integer(string="interval")

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

