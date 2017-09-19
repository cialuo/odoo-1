# -*- coding:utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime
import json
import collections
from utils import *

timeFormatStr = "%Y-%m-%d %H:%M:%S"

class BusWorkRules(models.Model):
    """
    行车规则
    """

    _name = 'scheduleplan.schedulrule'

    name = fields.Char(string="rule name", required=True)

    # 线路
    line_id = fields.Many2one("route_manage.route_manage", string="related line", readonly=True)

    def _defaultType(self):
        type = self._context.get('bustype', False)
        if type == 'normal':
            return 'normal'
        elif type == 'custem':
            return 'custem'

    active = fields.Boolean('Active', default=True)

    def toggle_active(self):
        return super(BusWorkRules, self).toggle_active()

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

    def getTargetDate(self):
        return '20170913'

    def getCityCode(self):
        return '130400'
        return self.env['ir.config_parameter'].get_param('city.code')

    def getAPIUrl(self):
        return self.env['ir.config_parameter'].get_param('bus.arrange.rule.url')

    @api.multi
    def fetchRuleFromBigData(self):
        """
        从大数据获取行车规则
        """
        url = self.getAPIUrl()
        datestr = self.getTargetDate()
        # data = getRuleFromBigData(url, 'sdf123', self.line_id.id, datestr, self.schedule_method)
        if self.schedule_method == 'singleway':
            schedule = 0
        else:
            schedule = 1
        try:
            data = getRuleFromBigData(url, self.getCityCode(), 10, datestr, 0)
        except Exception as e:
            raise
            raise ValidationError("failed to connect api server")
        if data == None:
            raise ValidationError(_("fetch data failed from bigdata system"))
        update = {}
        update['upplanvehiclearrange'] = data['vup']
        update['uptimearrange'] = data['tup']
        if len(data['vdown']) != 0:
            update['downplanvehiclearrange'] = data['vdown']
        if len(data['tdown']) != 0:
            update['downtimearrange'] = data['tdown']
        self.write(update)

    @staticmethod
    def _validateVehicleNums(obj):
        vcount = 0
        for item in obj.upplanvehiclearrange:
            vcount += item.allvehicles

        if obj.schedule_method == 'dubleway':
            for item in obj.downplanvehiclearrange:
                vcount += item.allvehicles

        if vcount > obj.bus_number:
            raise ValidationError(_("vechile count large then vehicle number"))

    def getBusMoveTimeInSpecialday(self, ruleid, datestr):
        """
        获取指定行车规则下的指定日期的行车时刻表
        :param ruleid: 规则id
        :param datestr: 日期字符串
        """
        result = self.env['scheduleplan.busmovetime'].search([('rule_id', '=', ruleid), ('executedate', '=', datestr)])
        if len(result) == 0:
            return None
        else:
            return result[0]

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
        """
        验证发车安排是否和线路的首班末班时间匹配
        :param datalist: 发车安排
        :param start: 首班时间
        :param end: 末班时间
        """
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
        # if len(dataList) <= 0:
        #     raise ValidationError(_("time arrange must not empty"))
        newlist = sorted(dataList, key=lambda k: k.seqid)
        # 验证序列号
        BusWorkRules._validate_sqenum(newlist)
        # 验证开始结束时间
        BusWorkRules._validate_startendtime(newlist, startTime, endTime)
        # 验证时间连续性
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
        """
        根据行车规则的发车安排生成每一趟发车时刻
        :param rulelist: 发车规则
        :param datestr: 规则日期
        :param startstation: 首发站
        :param endstation: 终点站
        :param lineid: 线路id
        :param mileage: 里程
        """
        sortedRuleList = sorted(rulelist, key=lambda k: k.seqid)
        recordslist = []
        if len(sortedRuleList) == 0 :
            return []
        startTimeStr = datestr + ' ' + sortedRuleList[0].starttime + ":00"

        startTime = datetime.datetime.strptime(startTimeStr, timeFormatStr)
        markpoints = []
        for item in sortedRuleList:
            markpoints.append((item.interval, datetime.datetime.strptime(datestr + ' ' + item.endtime + ":00", timeFormatStr)))
        seqcounter = 0
        for index, item in enumerate(sortedRuleList):
            while startTime < markpoints[index][1]:
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
        if startTime >= markpoints[-1][1]:
            # 如果最后一趟超出了计划时间的最后时间 则调整为计划最后发车时间
            startTime = markpoints[-1][1]
            data = {
                'seqid': seqcounter+1,
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
        """
        生成行车时刻表数据
        """
        for item in ruleobj:
            movetimerecord = {
                'name' : datestr + "/" +item.line_id.line_name,
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
            return res


    @classmethod
    def genExcuteRecords(cls, movetimeobj):
        """
        生成行车作业执行表数据
        """
        values = {
            'name' : movetimeobj.name,
            'excutedate' : movetimeobj.executedate,
            'line_id' : movetimeobj.line_id.id,
            'movetimetable_id':movetimeobj.id,
            'rule_id': movetimeobj.rule_id.id
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

        stafftimearrange, staffarrangeid = BusWorkRules.getBusStaffGroup(staffgroupmode,
                                                         movetimeobj.executedate,
                                                         movetimeobj.id)
        if stafftimearrange == False:
            return False
        # 关联的人车配班表记录
        values['staffarrangetable_id'] = staffarrangeid

        movetimelist = json.loads(movetimeobj.operationplan)

        # 上行行车执行记录
        upexeitems = BusWorkRules.genModedetailRecords(movetimelist['up'], stafftimearrange, movetimeobj.env['scheduleplan.movetimeup'])
        # 下行行车执行记录
        if movetimeobj.schedule_method == 'dubleway':
            downexeitems = BusWorkRules.genModedetailRecords(movetimelist['down'], stafftimearrange, movetimeobj.env['scheduleplan.movetimedown'])
        else:
            downexeitems = []
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
                conductorworklist[item[2]['steward']].append((item[2]['starttime'], item[2]['arrivetime'],item[2]['vehicle_id']))

        for item in downexeitems:
            if item[2]['driver']:
                driverworklist[item[2]['driver']].append((item[2]['starttime'], item[2]['arrivetime'],item[2]['vehicle_id']))
            if item[2]['steward']:
                conductorworklist[item[2]['steward']].append((item[2]['starttime'], item[2]['arrivetime'],item[2]['vehicle_id']))

        for k, v in driverworklist.items():
            driverworklist[k] = sorted(v, key=lambda x:x[0])

        for k, v in conductorworklist.items():
            conductorworklist[k] = sorted(v, key=lambda x:x[0])

        drivernum = 0
        conductornum = 0

        # 计算出勤司乘数据
        addrecords = []
        for k,v in conductorworklist.items():
            result = BusWorkRules.worksectionrecords(worksectionconductor[k],v)
            for item in result:
                value = {
                    'worktime': movetimeobj.executedate,
                    'vehicle_id' : v[-1][-1],
                    'title' : 'steward',
                    'employee_id' : k,
                    'checkintime' : item[1][0],
                    'checkouttime' : item[1][1],
                    'realworkstart' : item[0][0][0],
                    'realworkdone': item[0][1][1]
                }
                value['worktimelength'] = timesubtraction(item[1][1], item[1][0])
                value['workrealtimelength'] = timesubtraction(item[0][1][1], item[0][0][0])
                conductornum += 1
                addrecords.append((0,0,value))

        for k, v in driverworklist.items():
            result = BusWorkRules.worksectionrecords(worksectiondriver[k], v)
            for item in result:
                value = {
                    'worktime': movetimeobj.executedate,
                    'vehicle_id': v[-1][-1],
                    'title': 'driver',
                    'employee_id': k,
                    'checkintime': item[1][0],
                    'checkouttime': item[1][1],
                    'realworkstart': item[0][0][0],
                    'realworkdone': item[0][1][1]
                }
                value['worktimelength'] = timesubtraction(item[1][1],item[1][0])
                value['workrealtimelength'] = timesubtraction(item[0][1][1], item[0][0][0])
                drivernum += 1
                addrecords.append((0, 0, value))

        values['motorcyclistsTime'] = addrecords
        values['drivernum'] = drivernum
        values['stewardnum'] = conductornum

        busworklist = collections.defaultdict(list)
        # 生成车辆资源数据
        result = []
        for item in upexeitems:
            busworklist[item[2]['vehicle_id']].append([item[2]['starttime'], item[2]['arrivetime'], item[2]['taici']])
        for item in downexeitems:
            busworklist[item[2]['vehicle_id']].append([item[2]['starttime'], item[2]['arrivetime'], item[2]['taici']])
        for k, v in busworklist.items():
            temp = sorted(v, key=lambda x: x[0])
            temp = [temp[0], temp[-1]]
            recval = {
                'vehicle_id': k,
                'firstmovetime': temp[0][0],
                'lastmovetime': temp[-1][0],
                'worktimelength': timesubtraction(temp[-1][0], temp[0][0]),
                'arrangenumber': temp[0][2],
                'workstatus':stafftimearrange[temp[0][2]]['operation_state']
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
            spliter.append(worksection[item][0])
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
        """
        result = []
        for item in movetimelist:
            if item[1] == None or item[1] == -1:
                continue

            timerec = cls.getTimeRecordDetail(timerecmode, item[1]['id'])
            if timerec == None:
                continue
            if item[0] not in stafflist:
                continue
            value = {
                'seq_id':item[1]['seqid'],
                'vehicle_id': stafflist[item[0]]['vehicle_id'].id,
                'starttime': item[1]['startmovetime'],
                'arrivetime': item[1]['arrive_time'],
                'timelenght': timerec.timelength,
                'mileage' : timerec.mileage,
                'line_id' : timerec.line_id.id,
                'taici' : item[0]
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
            return False, None
        record = staffgroup[0]
        result = {}
        for item in record.vehicle_line_ids:
            temp = {}
            temp['vehicle_id'] = item.vehicle_id
            temp['operation_state'] = item.operation_state
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
                    # ！！！ *** 跨天bug待处理 ***** ！
                    timeend = str2datetime(datestr+ " "+ y.end_time + ':00')
                    timeend = timeend - datetime.timedelta(hours=8)
                    data['timelist'].append((timestart.strftime(timeFormatStr), timeend.strftime(timeFormatStr)))

                timelist[x.bus_shift_choose_line_id] = data
            temp['employees'] = timelist
            result[item.sequence] = temp
        return result, record.id

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
            ("type", 'in', [tomorrow_type, "Vacation", "General"])
        ]
        result = datetypemode.search(condition, order='priority', limit=1)

        if len(result) <= 0:
            return
        datatype = result[0]
        rulelist = rulemode.search([("date_type", '=', datatype.id),("active", "=", True)])
        for item in rulelist:
            mvtime = self._timeTableExist(tomorrow_str, item.id)
            if mvtime == None:
                mvtime = self.createMoveTimeRecord(tomorrow_str, item)
            # 生成人车配班数据
            self.env['bus_staff_group'].action_gen_staff_group(item.line_id,
                                                                           staff_date=datetime.datetime.strptime(
                                                                               tomorrow_str, "%Y-%m-%d"),
                                                                           operation_ct=mvtime.vehiclenums,
                                                                           move_time_id=mvtime,
                                                                           force=True)
            # 生成运营方案数据
            mvtime.genOperatorPlan()
            if self._execTableExist(tomorrow_str, item.id) == None:
                # 生成行车作业执行数据
                BusWorkRules.genExcuteRecords(mvtime)

    def _timeTableExist(self, datestr, ruleid):
        res = self.env['scheduleplan.busmovetime'].search([('executedate', '=', datestr), ('rule_id', '=', ruleid)])
        if len(res) == 0:
            return None
        else:
            return res

    def _execTableExist(self, datestr, ruleid):
        res = self.env['scheduleplan.excutetable'].search([('excutedate', '=', datestr), ('rule_id', '=', ruleid)])
        if len(res) == 0:
            return None
        else:
            return res[0]


class RuleBusArrangeUp(models.Model):

    """
    配车方案 上行
    """

    _name = "scheduleplan.up.rulebusarrange"


    rule_id = fields.Many2one("scheduleplan.schedulrule", string="related rule", ondelete="cascade")

    # 车型
    vehiclemode = fields.Many2one("fleet.vehicle.model", string="vehicle mode", required=True)

    # 运营数量
    workingnumber = fields.Integer(string="vehicle working number", required=True)

    # 机动车数量
    backupnumber = fields.Integer(string="vehicle backup number", required=True)

    # 核载人数
    passengernumber = fields.Integer(related="vehiclemode.ride_number", string="passenger number")

    # 车辆总数
    allvehicles = fields.Integer(compute="_sumvehicles", string="all vehcile number")

    @api.depends('workingnumber', 'backupnumber')
    def _sumvehicles(self):
        for item in self:
            item.allvehicles = item.workingnumber + item.backupnumber


class ToUp(models.Model):
    """
    上行发车安排
    """
    _name = "scheduleplan.toup"

    rule_id = fields.Many2one("scheduleplan.schedulrule", string="related rule", ondelete="cascade")

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
    worktimelength = fields.Integer(string="line work time length", required=True)

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
    @api.constrains('interval', 'starttime', 'endtime')
    def _check_interval(self):
        if self.interval <= 0:
            raise ValidationError(_("interval must be an positive integer"))
        if check_time_format(self.starttime) == None:
            raise ValidationError(_("time format error: ") + self.starttime)
        if check_time_format(self.endtime) == None:
            raise ValidationError(_("time format error: ") + self.endtime)

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

    rule_id = fields.Many2one("scheduleplan.schedulrule", string="related rule", ondelete="cascade")

    site_id = fields.Many2one("opertation_resources_station")

    # 站序
    site_seq = fields.Integer(string="site sequence")

    # 是否签点
    needsign = fields.Boolean(string="need sign")

    # 是否大站考核
    needchecking = fields.Boolean(string="need checking")

    # 距首站时间(低峰)
    tolastsit_low = fields.Integer(string="to last site time (low)")

    # 距首站时间(平峰)
    tolastsit_flat = fields.Integer(string="to last site time (flat)")

    # 距首站时间(高峰)
    tolastsit_peak = fields.Integer(string="to last site time (high)")

    # 允许快几分钟
    fastthen = fields.Integer(string="fast allowed")

    # 允许慢几分钟
    slowthen = fields.Integer(string="slow allowed")


class BigSiteSettingsDown(models.Model):

    _name = "scheduleplan.bigsitesetdown"

    _inherit = "scheduleplan.bigsitesetup"

