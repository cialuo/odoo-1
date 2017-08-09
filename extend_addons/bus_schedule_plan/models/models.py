# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime
from itertools import izip_longest
import json
import math

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

    # 线路
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

    # 日期类型
    date_type = fields.Many2one("bus_date_type", string="bus date type", required=True)


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
            if (datalist[i].seqid - datalist[i-1].seqid) != 1:
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
        if len(dataList) <= 0:
            return
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

    @staticmethod
    def targetDate(offset):
        """
        获取要计算的目标日期
        offset 为一个整数 为相对于今天的偏移量
        比如 计算明天 offset 就是 1 后天 offset就是2 昨天 offset就是-1
        """
        today = datetime.datetime.today()
        timedelta = datetime.timedelta(days=offset)
        return today + timedelta

    @staticmethod
    def mapWeekDayStr(daynumber):
        """
        将星期id转换为本系统的日期类型
        """
        mapdic = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

        return mapdic[daynumber]

    @staticmethod
    def formatDateStr(dateobj):
        """
        格式化日期
        """
        return dateobj.strftime("%Y-%m-%d")

    def genTimeRecords(self, rulelist, datestr, startstation, endstation, lineid, mileage):
        sortedRuleList = sorted(rulelist, key=lambda k: k.seqid)
        recordslist = []
        startTimeStr = datestr + ' ' + sortedRuleList[0].starttime + ":00"

        startTime = datetime.datetime.strptime(startTimeStr, timeFormatStr)
        markpoints = []
        for item in sortedRuleList:
            markpoints.append((item.interval, datetime.datetime.strptime(datestr + ' ' + item.endtime + ":00", timeFormatStr)))
        seqcounter = 0
        for index, item in enumerate(sortedRuleList):
            while startTime <= markpoints[index][1]:
                seqcounter += 1
                data = {
                    'seqid' : seqcounter,
                    'startmovetime' : startTime-datetime.timedelta(hours=8),
                    'arrive_time' : startTime + datetime.timedelta(minutes=item.worktimelength)-datetime.timedelta(hours=8),
                    'timelength' : item.worktimelength,
                    'mileage' : mileage,
                    'line_id' : lineid.id,
                    'start_site' : startstation.id,
                    'end_site' : endstation.id
                }
                recordslist.append((0, 0, data))
                startTime = startTime + datetime.timedelta(minutes=item.interval)
        return recordslist

        # 上行运营车辆数
        upworkvehicle = fields.Integer(string="up work vehicle")

        # 下行机动车辆数
        upbackupvehicle = fields.Integer(string="up backup vehicle")

        # 下行车辆数
        downworkvehicle = fields.Integer(string="down work vehicle")

        # 下行机动车辆数
        downbackupvehicle = fields.Integer(string="down backup vehicle")

    def createMoveTimeRecord(self, datestr, ruleobj):
        for item in ruleobj:
            movetimerecord = {
                'name' : datestr + item.line_id.lineName,
                'line_id' : item.line_id.id,
                'rule_id' : item.id,
                'vehiclenums' : 0,
                'backupvehicles' : 0,
                'executedate' : datestr,
                'schedule_method' : item.schedule_method,
                'upworkvehicle': 0,
                'upbackupvehicle' : 0,
                'downworkvehicle' : 0,
                'downbackupvehicle' : 0
            }
            vehiclenums = 0
            backupvehicles = 0
            if item.schedule_method == 'singleway':
                for i in item.upplanvehiclearrange:
                    movetimerecord['upworkvehicle'] += i.workingnumber
                    movetimerecord['upbackupvehicle'] += i.backupnumber
                    vehiclenums += i.workingnumber
                    backupvehicles += i.backupnumber
                    timerecords = self.genTimeRecords(item.uptimearrange, datestr, item.upstation, item.upstation,
                                                      item.line_id, item.mileage)
                    movetimerecord['uptimeslist'] = timerecords
            elif item.schedule_method == 'dubleway':
                for i in item.upplanvehiclearrange:
                    movetimerecord['upworkvehicle'] += i.workingnumber
                    movetimerecord['upbackupvehicle'] += i.backupnumber
                    vehiclenums += i.workingnumber
                    backupvehicles += i.backupnumber
                for i in item.downplanvehiclearrange:
                    movetimerecord['downworkvehicle'] += i.workingnumber
                    movetimerecord['downbackupvehicle'] += i.backupnumber
                    vehiclenums += i.workingnumber
                    backupvehicles += i.backupnumber
                uptimerecords = self.genTimeRecords(item.uptimearrange, datestr, item.upstation, item.downstation,
                                                        item.line_id, item.mileage)
                downtimerecords = self.genTimeRecords(item.downtimearrange, datestr, item.downstation,
                                                          item.upstation, item.line_id, item.mileage)
                movetimerecord['uptimeslist'] = uptimerecords
                movetimerecord['downtimeslist'] = downtimerecords

            movetimerecord['vehiclenums'] = vehiclenums
            movetimerecord['backupvehicles'] = backupvehicles
            res = self.env['scheduleplan.busmovetime'].create(movetimerecord)
            res.genOperatorPlan()

    def createMoveTimeTable(self):
        """
        生成行车时刻表
        """
        rulemode = self.env['scheduleplan.schedulrule']
        datetypemode = self.env['bus_date_type']
        tomorrow = BusWorkRules.targetDate(1)
        x = tomorrow.weekday()
        tomorrow_type = BusWorkRules.mapWeekDayStr(tomorrow.weekday())
        tomorrow_str = BusWorkRules.formatDateStr(tomorrow)
        condition = [
            ("start_date", '<=', tomorrow_str), ("end_date", '>=', tomorrow_str),
            '|', ("type", '=', tomorrow_type), ("type", '=', "Vacation")
        ]
        result = datetypemode.search(condition, order='priority desc', limit=1)

        if len(result) <= 0:
            return
        datatype = result[0]
        rulelist = rulemode.search([("date_type", '=', datatype.id)])
        for item in rulelist:
            self.createMoveTimeRecord(tomorrow_str, item)


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

    name = fields.Char(string="record name")

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

    # 运营计划 存储上下行车辆次序 存储json数据
    operationplan = fields.Text(string="operation plan")

    # 运营方案 存储每辆车的运行趟次列表
    operationplanbus = fields.Text(string="operation plan bus move")

    # 上行运营车辆数
    upworkvehicle = fields.Integer(string="up work vehicle")

    # 下行机动车辆数
    upbackupvehicle = fields.Integer(string="up backup vehicle")

    # 下行车辆数
    downworkvehicle = fields.Integer(string="down work vehicle")

    # 下行机动车辆数
    downbackupvehicle = fields.Integer(string="down backup vehicle")


    @staticmethod
    def genVehicleSeq(up, down=None):
        uprepeatSeq = []  # 上行轮换序列
        downrepeatSeq = []  # 下行轮换序列
        for i in range(1, up + 1):
            uprepeatSeq.append(i)
        if down!=None:
            for i in range(up + 1, up + 1 + down):
                downrepeatSeq.append(i)
        return uprepeatSeq, downrepeatSeq

    @staticmethod
    def genWorkMap(moveTimeSeq, repeatseq, direction):
        upworklen = len(moveTimeSeq)
        workBusSeq = repeatseq * int(math.ceil(upworklen / float(len(repeatseq))))
        workBusSeqDetail = []
        for busid, moveTimeObj in izip_longest(workBusSeq, moveTimeSeq):
            unit = [busid, None]
            if moveTimeObj != None:
                unit[1] = {'id': moveTimeObj.id,
                           'startmovetime': moveTimeObj.startmovetime,
                           'arrive_time': moveTimeObj.arrive_time,
                           'direction': direction}
            else:
                unit[1] = None
            workBusSeqDetail.append(unit)
        return workBusSeqDetail

    @staticmethod
    def genBusMoveSeqDouble(upMoveSeq, downMoveSeq, upBusCol, downBusCol):
        busCol = upBusCol + downBusCol
        moveseqCol = {busid:{'up':[],'down':[] } for busid in busCol}
        for index, item in enumerate(upMoveSeq):
            moveseqCol[item[0]]['up'].append([index, item, 'up'])

        for index , item in  enumerate(downMoveSeq):
            moveseqCol[item[0]['down']].append([index, item, 'down'])

        result = {}
        for (k, v) in moveseqCol.items():
            if k <= downMoveSeq[-1]:
                temp = []
                for x, y in izip_longest(v['up'], v['down']):
                    if x != None:
                        temp.append(x)
                    if y != None:
                        temp.append(y)
                result[k] = temp
            else:
                temp = []
                for x, y in izip_longest(v['down'], v['up']):
                    if x!= None:
                        temp.append(x)
                    if y != None:
                        temp.append(y)
                result[k] = temp
        return result

    @staticmethod
    def genBusMoveSeqsingle(upMoveSeq, upBusCol):
        busMoveSeq = {busid: [] for busid in upBusCol}
        for index, item in enumerate(upMoveSeq):
            busMoveSeq[item[0]].append([index, item])
        return busMoveSeq


    @staticmethod
    def culculateStopTime(busMoveTimeCol):
        for k, v in busMoveTimeCol.items():
            l = len(v)
            for index, item in enumerate(v):
                item.append(0)
                if item[1][1] == None:
                    continue
                for i in range(index+1, l):
                    if v[i][1][1] == None:
                        continue
                    stime = datetime.datetime.strptime(v[i][1][1]['startmovetime'], timeFormatStr)
                    atime = datetime.datetime.strptime(item[1][1]['arrive_time'], timeFormatStr)
                    item.append(stime - atime)
                    break


    # 生成运营方案数据
    def genOperatorPlan(self):
        upVechicleSeq, downVehicleSeq = self.genVehicleSeq(self.upworkvehicle, self.downworkvehicle)
        upRepeatSeq = upVechicleSeq + downVehicleSeq
        downRepeatSeq = downVehicleSeq + upVechicleSeq

        upMoveOnSeq = self.genWorkMap(self.uptimeslist, upRepeatSeq, 'up')
        downMoveOnSeq = None
        if self.schedule_method == 'dubleway':
            downMoveOnSeq = self.genWorkMap(self.downtimeslist, downRepeatSeq, 'down')

        operationPlan = {'up':upMoveOnSeq, 'down':downMoveOnSeq}
        busMoveTable = None
        if self.schedule_method == 'dubleway':
            busMoveTable = self.genBusMoveSeqDouble(upMoveOnSeq, downMoveOnSeq, upVechicleSeq, downVehicleSeq)
        elif self.schedule_method == 'singleway':
            busMoveTable = self.genBusMoveSeqsingle(upMoveOnSeq, upVechicleSeq)

        self.operationplanbus = json.dumps(busMoveTable)

        self.operationplan = json.dumps(operationPlan)

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