# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime
from itertools import izip_longest
import json
import math
import collections

timeFormatStr = "%Y-%m-%d %H:%M:%S"

def str2datetime(timestr):
    return datetime.datetime.strptime(timestr,timeFormatStr)

def timesubtraction(time1, time2):
    time1 = str2datetime(time1)
    time2 = str2datetime(time2)
    return round((time1 - time2).total_seconds()/3600.00,1)

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
        if startTime != markpoints[-1][1]:
            data = {
                'seqid': seqcounter,
                'startmovetime': startTime - datetime.timedelta(hours=8),
                'arrive_time': startTime + datetime.timedelta(minutes=sortedRuleList[-1].worktimelength) - datetime.timedelta(
                    hours=8),
                'timelength': sortedRuleList[-1].worktimelength,
                'mileage': mileage,
                'line_id': lineid.id,
                'start_site': startstation.id,
                'end_site': endstation.id
            }
            recordslist.append((0, 0, data))
        return recordslist


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
            # 生成人车配班数据
            staffdata = self.env['bus_staff_group'].action_gen_staff_group(item.line_id,
                                                               staff_date=datetime.datetime.strptime(datestr, "%Y-%m-%d"),
                                                               operation_ct=vehiclenums, move_time_id=res, force=True)
            res.genOperatorPlan()
            BusWorkRules.genExcuteRecords(res)

    @classmethod
    def genExcuteRecords(cls, movetimeobj):
        """
        生成行车记录执行表
        """
        values = {
            'name' : movetimeobj.name,
            'excutedate' : movetimeobj.executedate,
            'line_id' : movetimeobj.line_id.id,
        }
        # 生成上行时刻表列表并排序
        uptimelist = [item for item in movetimeobj.uptimeslist]
        uptimelist = sorted(uptimelist, key=lambda x: x.seqid)
        # 生成下行时刻表列表并排序
        downtimelist = [item for item in movetimeobj.downtimeslist]
        downtimelist = sorted(downtimelist, key=lambda x: x.seqid)

        # 上行首班时间
        values['firstruntime'] = uptimelist[0]['startmovetime'] if len(uptimelist) > 0 else False
        # 上行末班时间
        values['lastruntime'] = uptimelist[-1]['startmovetime'] if len(uptimelist) > 0 else False
        # 下行首班时间
        values['downfirstruntime'] = downtimelist[0]['startmovetime'] if len(downtimelist) > 0 else False
        # 下行末班时间
        values['downlastruntime'] = downtimelist[-1]['startmovetime'] if len(downtimelist) > 0 else False
        # 上行趟次
        values['upmovenum'] =  len(uptimelist)
        # 下行趟次
        values['downmovenum'] = len(downtimelist)
        # 运营车辆
        values['workvehiclenum'] = movetimeobj.vehiclenums
        # 机动车辆
        values['backupvehiclenum'] = movetimeobj.backupvehicles
        staffgroupmode = movetimeobj.env['bus_staff_group']
        stafftimearrange = BusWorkRules.getBusStaffGroup(staffgroupmode,
                                                         movetimeobj.executedate,
                                                         movetimeobj.id)
        if stafftimearrange == False:
            return False

        movetimelist = json.loads(movetimeobj.operationplan)

        upexeitems = BusWorkRules.genModedetailRecords(movetimelist['up'], stafftimearrange, movetimeobj.env['scheduleplan.movetimeup'])
        downexeitems = BusWorkRules.genModedetailRecords(movetimelist['down'], stafftimearrange, movetimeobj.env['scheduleplan.movetimedown'])
        # 上行排班计划
        values['upmoveplan'] = upexeitems
        # 下行排班计划
        values['downmoveplan'] = downexeitems

        worksectiondriver, worksectionconductor = BusWorkRules.staffWorkSection(stafftimearrange)

        driverworklist = collections.defaultdict(list)
        conductorworklist = collections.defaultdict(list)

        for item in upexeitems:
            if item[2]['driver']:
                driverworklist[item[2]['driver']].append((item[2]['starttime'], item[2]['arrivetime'],item[2]['vehicle_id']))
            if item[2]['steward']:
                conductorworklist[item[2]['steward']].append((item[2]['starttime'], item[2]['arrivetime']))

        for item in downexeitems:
            if item[2]['driver']:
                driverworklist[item[2]['driver']].append((item[2]['starttime'], item[2]['arrivetime'],item[2]['vehicle_id']))
            if item[2]['steward']:
                conductorworklist[item[2]['steward']].append((item[2]['starttime'], item[2]['arrivetime']))

        for k, v in driverworklist.items():
            driverworklist[k] = sorted(v, key=lambda x:x[0])

        for k, v in conductorworklist.items():
            conductorworklist[k] = sorted(v, key=lambda x:x[0])

        addrecords = []
        for k,v in conductorworklist.items():
            result = BusWorkRules.worksectionrecords(worksectionconductor[k],v)
            for item in result:
                value = {
                    'worktime': movetimeobj.executedate,
                    'vehicle_id' : item[-1],
                    'title' : 'steward',
                    'employee_id' : k,
                    'checkintime' : item[1][0],
                    'checkouttime' : item[1][1],
                    'realworkstart' : item[0][0][0],
                    'realworkdone': item[0][1][1]
                }
                value['worktimelength'] = timesubtraction(item[1][1], item[1][0])
                value['workrealtimelength'] = timesubtraction(item[0][1][1], item[0][0][0])
            addrecords.append((0,0,value))

        for k, v in driverworklist.items():
            result = BusWorkRules.worksectionrecords(worksectiondriver[k], v)
            for item in result:
                value = {
                    'worktime': movetimeobj.executedate,
                    'vehicle_id': item[-1],
                    'title': 'driver',
                    'employee_id': k,
                    'checkintime': item[1][0],
                    'checkouttime': item[1][1],
                    'realworkstart': item[0][0][0],
                    'realworkdone': item[0][1][1]
                }
                x = item[1][1]
                y = item[1][0]
                a = item[0][1][1]
                b = item[0][0][0]
                value['worktimelength'] = timesubtraction(item[1][1],item[1][0])
                value['workrealtimelength'] = timesubtraction(item[0][1][1], item[0][0][0])
                addrecords.append((0, 0, value))
        values['motorcyclistsTime'] = addrecords

        busworklist = collections.defaultdict(list)
        result = []
        for item in upexeitems:
            busworklist[item[2]['vehicle_id']].append([item[2]['starttime'], item[2]['arrivetime']])
        for item in downexeitems:
            busworklist[item[2]['vehicle_id']].append([item[2]['starttime'], item[2]['arrivetime']])
        for k, v in busworklist.items():
            temp = sorted(v, key=lambda x: x[0])
            temp = [temp[0], temp[-1]]
            recval = {
                'vehicle_id':k,
                'firstmovetime':temp[0][0],
                'lastmovetime':temp[-1][0],
                'worktimelength': timesubtraction(temp[-1][0], temp[0][0])
            }
            result.append((0,0,recval))
        values['vehicleresource'] = result

        movetimeobj.env['scheduleplan.excutetable'].create(values)

    @classmethod
    def worksectionrecords(cls, worksection, worklist):
        """
        由于一个司机可能在一天上多个班次 比如 上午九点到十二点 晚上八点到晚上十二点
        这个函数就是计算出司乘人员一天中的所有上车区间
        """
        spliter = []
        for item in range(1, len(worksection)):
            spliter.append(item[0])
        spliter.append(-1)
        result = []
        temp = []
        for i, item in enumerate(spliter):
            for x in worklist:
                if item == -1 or x[0] < item:
                    temp.append(x)
                else:
                    result.append([[temp[0], temp[-1]], worksection[i]])
                    temp=[]
                    temp.append(x)
                    break
        result.append([[temp[0], temp[-1]], worksection[-1], temp[0][-1]])
        return result



    @classmethod
    def staffWorkSection(cls, data):
        resultdriver = collections.defaultdict(list)
        resultconductor = collections.defaultdict(list)

        for item in data:
            employee = data[item]['employees']
            for _, x in employee.items():
                for y in x['timelist']:
                    if x['driver'] != False:
                        resultdriver[x['driver']].append(y)
                    if x['conductor'] != False:
                        resultconductor[x['conductor']].append(y)

        for k,v in resultdriver.items():
            resultdriver[k] = sorted(v, key=lambda x:x[0])
        for k,v in resultconductor.items():
            resultconductor[k] = sorted(v, key=lambda x:x[0])
        return resultdriver, resultconductor



    @classmethod
    def genModedetailRecords(cls, movetimelist, stafflist, timerecmode):
        """
        根据运营计划生成司机 售票员趟次数据
        :param movetimelist:
        :param stafflist:
        :param timerecmode:
        :return:
        """
        result = []
        for item in movetimelist:
            if item[1] == None:
                continue

            timerec = cls.getTimeRecordDetail(timerecmode, item[1]['id'])
            if timerec == None:
                # a = 99885
                continue

            value = {
                'seq_id':item[1]['seqid'],
                'vehicle_id': stafflist[item[0]]['vehicle_id'].id,
                'starttime': item[1]['startmovetime'],
                'arrivetime': item[1]['arrive_time'],
                'timelenght': timerec.timelength,
                'mileage' : timerec.mileage,
                'line_id' : timerec.line_id.id
            }
            driver, steward = cls.searchDriverAndSteward(item[1]['startmovetime'], stafflist[item[0]])
            value['driver'] = driver
            value['steward'] = steward
            result.append((0,0,value))
        return result

    @classmethod
    def searchDriverAndSteward(cls, startime, data):
        driver = None
        steward = None
        breakflag = False

        for k, v in data['employees'].items():
            if breakflag == True:
                break
            for x in v['timelist']:
                if startime >= x[0]  and startime <= x[1]:
                    driver = v['driver']
                    steward = v['conductor']
                    breakflag = True
                    break
        return driver, steward



    @classmethod
    def getTimeRecordDetail(cls, mode, id):
        record = mode.search([('id', '=', id)])
        if len(record) == 0:
            return None
        return record


    @classmethod
    def getBusStaffGroup(cls, staffgroupmode, datestr, movetimeid):
        """
        获取人车配班列表信息
        """
        staffgroup = staffgroupmode.search([('move_time_id', '=', movetimeid)])
        if len(staffgroup) == 0:
            return False
        record = staffgroup[0]
        result = {}
        for item in record.vehicle_line_ids:
            temp = {}
            temp['vehicle_id'] = item.vehicle_id
            timelist = {}
            for x in item.staff_line_ids:
                data = {'driver': x.driver_id.id,
                        'conductor': x.conductor_id.id,
                        'timelist' : []
                        }
                for y in x.bus_shift_choose_line_id.shift_line_id.detail_ids:
                    # 修正到utc时间
                    timestart = str2datetime(datestr+ " "+ y.start_time + ':00')
                    timestart = timestart - datetime.timedelta(hours=8)
                    timeend = str2datetime(datestr+ " "+ y.end_time + ':00')
                    timeend = timeend - datetime.timedelta(hours=8)
                    data['timelist'].append((timestart.strftime(timeFormatStr), timeend.strftime(timeFormatStr)))

                timelist[x.bus_shift_choose_line_id] = data
            temp['employees'] = timelist
            result[item.sequence] = temp
        return result

    def createMoveTimeTable(self):
        """
        生成行车时刻表
        """
        rulemode = self.env['scheduleplan.schedulrule']
        datetypemode = self.env['bus_date_type']
        tomorrow = BusWorkRules.targetDate(1)
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
                           'seqid': moveTimeObj.seqid,
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
            moveseqCol[item[0]]['down'].append([index, item, 'down'])

        result = {}
        for (k, v) in moveseqCol.items():
            if k <= upBusCol[-1]:
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
    """
    行车作业执行表
    """
    _name = "scheduleplan.excutetable"

    name = fields.Char(string="excute table name")

    # 线路
    line_id = fields.Many2one("route_manage.route_manage", string="related line")

    # 状态
    status = fields.Selection([("draft", "draft"),              # 草稿
                                ("wait4use", "wait for use"),   # 待使用
                                ("done", "done"),               # 完成
                              ], default="wait4use",  string="status")

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

    execplan_id = fields.Many2one("scheduleplan.excutetable")

    # 序号
    seq_id = fields.Integer(string="sequence id")

    vehicle_id = fields.Many2one("fleet.vehicle")

    # 车辆编号
    # vehiclecode = fields.Char(related="fleet.vehicle", string="vehicle code number")

    # 司机
    driver = fields.Many2one("hr.employee", string="dirver")

    # 乘务员
    steward = fields.Many2one("hr.employee", string="steward")

    # 发车时间
    starttime = fields.Datetime(string="start move time")

    # 到达时间
    arrivetime = fields.Datetime(string="arrive time")

    # 时长 分钟记
    timelenght = fields.Integer(string="time length (min)")

    # 里程
    mileage = fields.Integer(string="mileage number")

    # 线路
    line_id = fields.Many2one("route_manage.route_manage", string="related line")


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

    execplan_id = fields.Many2one("scheduleplan.excutetable")

    employee_id = fields.Many2one("hr.employee", string="emplyee id")

    # 日期
    worktime = fields.Date(string="work date")

    vehicle_id = fields.Many2one("fleet.vehicle")

    # 车辆编号
    # vehiclecode = fields.Char(related="fleet.vehicle", string="vehicle code number")

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

    execplan_id = fields.Many2one("scheduleplan.excutetable")

    vehicle_id = fields.Many2one("fleet.vehicle")

    # 车辆编号
    # vehiclecode = fields.Char(related="vehicle_id.inner_code", string="vehicle code number")

    # 首班发车时间
    firstmovetime = fields.Datetime(string="first move time")

    # 末班发车时间
    lastmovetime = fields.Datetime(string="last move time")

    # 运营时长
    worktimelength = fields.Float(string="work time length")
