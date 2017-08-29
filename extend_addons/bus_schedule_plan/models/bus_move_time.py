# -*- coding:utf-8 -*-
from odoo import models, fields, api, _
from utils import *
import math
from itertools import izip_longest

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

    @api.multi
    def genStaffArrange(self):
        staffdata = self.env['bus_staff_group'].action_gen_staff_group(self.line_id,
                                                                       staff_date=datetime.datetime.strptime(
                                                                           self.executedate, "%Y-%m-%d"),
                                                                       operation_ct=self.vehiclenums,
                                                                       move_time_id=self,
                                                                       force=True)
        return

    @staticmethod
    def genVehicleSeq(up, down=None):
        uprepeatSeq = []  # 上行轮换序列
        downrepeatSeq = []  # 下行轮换序列

        if down!=None:
            for i in range(1, down + 1):
                downrepeatSeq.append(i)
        for i in range(down + 1, down + up + 1):
            uprepeatSeq.append(i)

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
                # t = [g for g in izip_longest(v['down'], v['up'])]
                for x, y in izip_longest(v['down'], v['up']):
                    if x!= None:
                        temp.append(x)
                    if y != None:
                        temp.append(y)
                result[k] = temp
        return result

    @classmethod
    def genWebRetunData(cls, data4direction, dataforbus, upstation, downstation):
        data = {
            'direction':data4direction,
            'bus':dataforbus,
            'upstation':upstation,
            'downstation':downstation
        }
        return data

    @classmethod
    def preprocess2WebData(cls, data):
        """
        对返回给客户端的运营数据做预处理
        """
        for item in data.values():
            for x in item:
                if x[1][1] != None:
                    x[1][1]['arrive_time'] = adjustDateTime2ZhCn(x[1][1]['arrive_time'])
                    x[1][1]['startmovetime'] = adjustDateTime2ZhCn(x[1][1]['startmovetime'])
        return data

    @api.model
    def reoppaln2web(self, recid):
        """
        返回运营方案数据到web前端
        """
        row = self.search([('id', '=', recid)])
        row = row[0]
        try:
            arg1 = json.loads(row.operationplan)
        except Exception:
            arg1 = {}
        try:
            arg2 = json.loads(row.operationplanbus)
            arg2 = self.preprocess2WebData(arg2)
        except Exception as e:
            arg2 = {}
        station1 = row.line_id.up_station.name
        station2 = row.line_id.down_station.name
        return self.genWebRetunData(arg1, arg2, station1, station2)

    @classmethod
    def rebuildOpPlanAdd(cls, data, index, seq):
        for i in range(index+1, len(data)):
            temp = data[i][1]
            data[i-1][1] = temp
        data[-1][1] = None
        num = 0
        for i in range(len(data)-1, 0, -1):
            if data[i][1] != None:
                num += 1
            else:
                break
        # 去掉尾部为None的序列
        if num / len(seq) > 0:
            data = data[0:-((num / len(seq)) * len(seq))]

        return data

    @classmethod
    def rebuildOpPlanRemove(cls, data, index, seq):
        if data[-1][1] != None:
            for item in seq:
                data.append([item, None])
        pre = None
        for i in range(index, len(data)):
            temp = data[i][1]
            data[i][1] = pre
            pre = temp
        return data



    @api.model
    def changeOpplan(self, recid, index, direction, data, op):
        # 修改运营计划
        row = self.search([('id', '=', recid)])
        row = row[0]
        upVechicleSeq, downVehicleSeq = self.genVehicleSeq(row.upworkvehicle, row.downworkvehicle)
        upRepeatSeq = upVechicleSeq + downVehicleSeq
        downRepeatSeq = downVehicleSeq + upVechicleSeq
        result = None
        if direction == 'up':
            if op == 0:
                result = self.rebuildOpPlanRemove(data['up'], index, upRepeatSeq)
            else:
                result = self.rebuildOpPlanAdd(data['up'], index, upRepeatSeq)
            data['up'] = result
        elif direction == 'down':
            if op == 0:
                result = self.rebuildOpPlanRemove(data['down'], index, downRepeatSeq)
            else:
                result = self.rebuildOpPlanAdd(data['down'], index, downRepeatSeq)
            data['down'] = result

        busMoveTable = None
        if data['down'] != None:
            # 双头调
            busMoveTable = self.genBusMoveSeqDouble(data['up'], data['down'], upVechicleSeq, downVehicleSeq)
        elif self.schedule_method == 'singleway':
            # 单头调
            busMoveTable = self.genBusMoveSeqsingle(data['up'], upVechicleSeq)
        busMoveTable = self.culculateStopTime(busMoveTable)
        station1 = row.line_id.up_station.name
        station2 = row.line_id.down_station.name
        return self.genWebRetunData(data, busMoveTable, station1, station2)

    @api.model
    def saveOpPlan(self):
        """
        保存运营方案数据
        """
        return json.dumps({})

    @staticmethod
    def genBusMoveSeqsingle(upMoveSeq, upBusCol):
        busMoveSeq = {busid: [] for busid in upBusCol}
        for index, item in enumerate(upMoveSeq):
            busMoveSeq[item[0]].append([index, item])
        return busMoveSeq


    @classmethod
    def culculateStopTime(cls, busMoveTimeCol):
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
                    item.append((stime - atime).total_seconds()/60)
                    break
        return busMoveTimeCol


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

        busMoveTable = self.culculateStopTime(busMoveTable)

        self.operationplanbus = json.dumps(busMoveTable)

        self.operationplan = json.dumps(operationPlan)


class MoveTimeUP(models.Model):

    _name = "scheduleplan.movetimeup"

    movetimetable_id = fields.Many2one("scheduleplan.busmovetime", ondelete="cascade")

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

