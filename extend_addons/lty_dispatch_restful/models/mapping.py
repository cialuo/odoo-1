# -*- coding: utf-8 -*-
##############################################################################
#
#
#    Copyright (C) 2017 xiao (715294035@qq.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.
#
##############################################################################
import logging

_logger = logging.getLogger(__name__)

#线路基础数据
# op_line
op_line = {
    #线路ID
    ('id', 'id'): None,
    #线路编码
    ('gprsId', 'gprs_id'): None,
    #线路名称
    ('lineName', 'line_name'): None,
    #线路类型，无对应字段（1：单向环线；2：双向环线；3：双向线路）
    ('lineTypeId', None): None,
    #调车方式
    ('runTypeId', 'run_type_name'): {'single_shunt': 1, 'double_shunt':2},
    #调度类型
    ('dispatchModeId', 'schedule_type'): {'flexible_scheduling': 1003, 'planning_scheduling': 1004, 'hybrid_scheduling': 2027},
    #文档中提供的班制是 001,002,003 不符合文档中提供的类型long,改成1,2,3,
    ('classSystemId', 'classSystemName'): {'one_shift': 1, 'two_shift': 2, 'three_shift': 3},
    #文档提供的类型是Long，提供 部门ID
    ('departmentId', 'department_id'): None,
    #是否环线，无对应字段（0：环线；1：非环线）,默认传值：0
    ('isRoundLine', None): None,
    #是否夜班线路，无对应字段（0：非夜班；1：夜班线路）,默认传值：0
    ('isNight', None): None,
    #是否跨天，无对应字段(0：跨天；1：非跨天),默认传值：0
    ('isCrossDay', None): None,
    #票价，无对应字段
    ('ticketPrice', None): None,
    #线路开通日期，无对应字段
    ('startDate', None): None,
    #线路停运日期，无对应字段
    ('endDate', None): None,
    #是否人工售票，无对应字段（0：非人工；1：人工售票）
    ('isArtificialTicket', None): None,
    #是否显示线路辅助点，无对应字段（0：不显示；1：显示）,默认传值：0
    ('isShowPoint', None): None,
    #是否显示站点名，无对应字段（0：不显示；1：显示）,默认传值：0
    ('isShowStationName', None): None,
    #以下三个字段文档未描述
    # 'lineStart': '',
    # 'lineEnd': '',
    # 'companyId': '',
}

#站台基础数据
# op_stationblock
op_stationblock = {
    ('id', 'id'): None,
    #站台编码
    ('stationId', 'code'): None,
    #站台名称
    ('stationName', 'name'): None,
    #地址,无对应字段
    ('address', None): None,
    #附近,无对应字段
    ('nearby', None): None,
    #经度
    ('longitude', 'longitude'): None,
    #纬度
    ('latitude', 'latitude'): None,
}
#站点基础数据 对应上下行站台两张表，会有重复数据库ID
# op_station
op_station = {
    ('id', 'id'): None,
    #线路编码int
    ('gprsId', None): None,
    #站点名称string
    ('stationName', None): None,
    #站点方案Id int
    ('opStationMainId', None): None,
    #线路Id int
    ('lineId', None): None,
    #站序 int
    ('orderNo', None): None,
    #方向 0:上行，1：下行
    ('direction', None): None,
    #站台id int
    ('blockId ', None): None,
    #距起点站距离 float
    ('byStartDistance', None): None,
    #进站经度 float
    ('longitude', None): None,
    #进站纬度 float
    ('latitude', None): None,
    #进站角度 int
    ('angle', None): None,
    #出站经度 float
    ('longitudeOut', None): None,
    #出站纬度 float
    ('latitudeOut', None): None,
    #出站角度 int
    ('angleOut', None): None,
    #距下一站时间
    ('toNextTime', None): None,

}
#车辆基础数据
# tjs_car
tjs_car = {
    ('id', 'id'): None,
    # #线路编码，无对应字段，不传
    # ('modelArgId', None): None,
    #线路ID
    ('lineId', 'route_id'): None,
    #车辆状态编码,文档中提供的是 001,002,003，004，不符合文档中提供的类型long，改为1,2,3,4
    ('carStateId', 'state'): {'normal': 3, 'repair': 1, 'stop': 4},
    #设备号，无对应字段
    ('onBoardId', None): None,
    #车辆编号
    ('carNum', 'inner_code'): None,
    #车辆牌照
    ('licensePlate', 'license_plate'): None,
    #发动机号
    ('engineNo', 'engine_no'): None,
    #是否营运
    ('ifService', 'vehicle_life_state'): {'operation_period': 0, 'invest_period': 1, 'scrap_period': 1},
    #载客数
    ('Zkrs', 'ride_number'): None,
    #座位数
    ('Zws', 'seats_ext'): None,
    #总运营公里
    ('Zyygl', 'total_odometer'): None,
    #车辆类型
    ('typeId', 'model_id'): None,
    #客门形式ID，无在对应字段；（1:1前2后；2:2前2后；3:2前1后；4:2前2后），2,4重复，默认传值：1
    ('doorTypeId', None): None,

}

#人员基础数据
# hr_employee
hr_employee = {
    ('id', 'id'): None,
    #用户编号，无对应字段，ODOO中用户编码为string，使用登录用户ID，
    ('userId', 'user_id'): None,
    #用户名称
    ('userStateName', 'name'): None,
    #手机号码
    ('mobilePhone', 'mobile_phone'): None,
    #邮箱
    ('email', 'work_email'): None,
    #工号
    ('Serils', 'jobnumber'): None,
    #员工类型编码，无对应字段，使用岗位ID
    ('sysPostId', 'workpost'): None,
    #IC卡号
    ('ICCardNoId', 'iccard'): None,
    #身份证
    ('sfz', 'id_card'): None,
}

#线路计划基础数据
# op_linePlan
op_lineplan = {
    ('id', 'id'): None,
    #编号，无对应字段,传ID
    ('serialNumber', 'id'): None,
    #线路 ID
    ('lineId', 'line_id'): None,
    #线路编码，无对应字段,后台取值
    ('gprsID', None): None,
    # 调车方式，无对应字段
    ('runTypeId', None): None,
    #调度类型编码
    ('dispatchModeId', None): None,
    #计划名称
    ('planName', 'name'): None,
    #上行里程，无对应字段
    ('runKmU', None): None,
    #下行里程，无对应字段
    ('runKmD', None): None,
    #上行首班时间 Datetime
    ('firstTime', 'firstruntime'): None,
    #上行末班时间 Datetime
    ('lastTime', 'lastruntime'): None,
    #计划趟次
    ('planCount', 'totalmovenum'): None,
    #下行首班时间 Datetime
    ('firstTimeD', 'downfirstruntime'): None,
    #下行末班时间 Datetime
    ('lastTimeD', 'downlastruntime'): None,
    #开始计划 Datetime
    ('startPlanTime', 'excutedate'): None,
    #创建日期
    ('createDate', 'create_date'): None,
    #主场站ID，无对应字段
    ('mainFieldId', None): None,
    #副场站ID，无对应字段
    ('viceFieldId', None): None,

}

#大站设置 无对应的表
# op_planstationbigmain
op_planstationbigmain = {
    #id string
    ('id', 'id'): None,
    #运营计划ID int
    ('linePlanId', None): None,
    #方案站点ID int
    ('opStationMainId', None): None,
    #站点ID int
    ('stationId', None): None,
    #站点名称
    ('stationName', None): None,
    #距起点站距离float
    ('byStartDistance', None): None,
    #是否大站考核,0:否，1：是
    ('isCheck', None): None,
    #是否签点,0：否，1：是
    ('isDispatchStation', None): None,
    #允许快几分钟 int
    ('fastTime', None): None,
    #允许慢几分钟 int
    ('slowTime', None): None,
    #方向 int
    ('Direction', None): None,
    #编号 int
    ('orderNo', None): None,
    #峰段标志ID 1:低峰；2：平峰；3：高峰
    ('flagId', None): None,
    #峰段标志名称 string
    ('flagName', None): None,
    #到下站考核时间点 string
    ('checkTime', None): None,
}

#调度线路基础数据 无对应的数据库表
# op_DspLine
op_dspLine = {
    ('id', 'id'): None,
    #名称 int
    ('lineId', None): None,
    #调度服务Id int
    ('dspId', None): None,
    #线路名称 string
    ('lineName', None): None,
    #方向int  必填;0：上行；1：下行
    ('direction', None): None,
    #车场编码long 必填;文档要求long，提供的为001：起始站,002：途中站,003：终点站
    ('fieldNo', None): None,
    #车场名称String
    ('fieldName', None): None,
    #屏幕1 int
    ('screen1', None): None,
    #屏幕2 int
    ('screen2', None): None,

}


#调度参数基础数据
#由于参数在不同的Model定义，只能从res.company取值，则只有 write 接口
# op_param
op_param = {
    ('id', 'id'): None,
    #名称，无对应字段
    ('lineId', None): None,
    #是否允许发送计划给车辆
    ('isSendPlan', 'is_send_plan_to_vehicle'): {True: 1, False:0},
    #提前发送计划给车辆的分钟数
    ('aheadSendPlan', 'send_plan_advance_time'): None,
    #是否允许发送计划给调度屏,不在调度参数表，在通用设置表
    ('isSendPlanV', 'is_send_the_plan'): {True: 1, False:0},
    #提前发送计划给调度屏的分钟数,不在调度参数表，在通用设置表
    ('aheadSendPlanV', 'send_time_in_advance'): None,
    #调度计划执行设置 计划超时判断,不在调度参数表，在通用设置表
    ('planTimeOut', 'plan_timeout_judgment'): None,
    #计划执行方式,不在调度参数表，在通用设置表
    ('planExeStyle', 'plan_execution_mode'): {'earliest': 1, 'recent':0},
    #计划显示范围, 无对应字段
    ('planViewRange', None): None,
    #同意请求排班
    ('agreeReqWorkPlan', 'is_agree_ask'): {True: 0, False:1},
    #签到立即派班
    ('signWorkPlan', 'is_attendance_ask'): {True: 1, False:0},
    #签到更新司机,不在调度参数表，在通用设置表
    ('signInUpdateDirver', 'is_check_replacement_driver'): {True: 1, False:0},
    #签到成功自动派班,重复
    # ('signWorkPlan', None): None，
    #不签到不派班
    ('noSignNoPlan', 'is_unattendance_ask'): {True: 1, False:0},
    #加油开始
    ('startRefuel', 'start_refueling'): {True: 0, False:1},
    #加油结束
    ('endRefuel', 'refueling_ended'): {True: 0, False:1},
    #维修开始
    ('startRepair', 'start_maintenance'): {True: 1, False:0},
    #维修结束
    ('endRepair', 'maintenance_ended'): {True: 1, False:0},
    #空放开始
    ('startSpare', 'start_release'): {True: 1, False:0},
    #空放结束
    ('endSpare', 'release_ended'): {True: 1, False:0},
    #保养开始, 无对应字段
    ('startMaintain', None): None,
    # 保养开始, 无对应字段
    ('endMaintain', None): None,
    # 保养开始, 无对应字段
    ('startMedicalCare', None): None,
    # 保养开始, 无对应字段
    ('endMedicalCare', None): None,
    #有效进出场范围,不在调度参数表，在通用设置表
    ('enterOrLeaveTime', 'effective_access'): None,
    #进场检测计划的范围 最小,不在调度参数表，在通用设置表
    ('enterCheckMin', 'in_station_min'): None,
    #进场检测计划的范围 最大（分钟）,不在调度参数表，在通用设置表
    ('enterCheckMax', 'in_station_max'): None,
    #出场带走计划的范围 最小（分钟）,不在调度参数表，在通用设置表
    ('leaveTakeMin', 'played_away_min'): None,
    #出场带走计划的范围 最大（分钟）,不在调度参数表，在通用设置表
    ('leaveTakeMax', 'played_away_max'): None,
    #提前发车判断（分钟）,不在调度参数表，在通用设置表
    ('earlyDeparture', 'ahead_of_departure_to_determine'): None,
    #缓后发车判断（分钟）
    ('delayedDeparture', 'slow_after_the_start_to_determine'): None,
    #取消发车计划时向司机发送短消息
    ('cancelGridPlan', 'cancel_departure_plan'): {True: 1, False:0},
    #向司机发送短消息 司机上班签到时
    ('driverSingin', 'driver_command'): {True: 1, False:0},
    #向司机发送短消息 司机下班签到时
    ('driverSingout', 'driver_checked_out'): {True: 1, False:0},
    #:向司机发送短消息 安排司机短休时
    ('arrangeDriverRest', 'driver_short_break'): {True: 1, False:0},
    #有效进出场范围,重复
    # ('enterOrLeaveTime', 'effective_access'): None,
    #驾驶员晚点预留,不在调度参数表，在通用设置表
    ('driverDelayedTime', 'driver_reserved_later'): None,
    #非运营限速值,不在调度参数表，在通用设置表
    ('notOpareLimitSpeed', 'operational_speed_limit'): None,
    #包车限速值,不在调度参数表，在通用设置表
    ('charteredLimitSpeed', 'chart_speed_limit'): None,
    #自动同步运营状态,文档要求Int，ODOO提供Boolean
    ('autoSyncStatus', 'is_automatically_synchronize_operational_status'): {True: 1, False:0},
    #自动同步车辆路线,文档要求Int，ODOO提供Boolean
    ('autoSyncLine', 'is_automatically_synchronize_lines'): {True: 1, False:0},
    #向司机发送短消息 车辆超载时,文档要求Int，ODOO提供Boolean
    ('busOverLoading', 'vehicle_overload'): {True: 1, False:0},
    #发车计划误点时,文档要求Int，ODOO提供Boolean
    ('delayedDeparturePlan', 'plan_to_be_delayed'): {True: 1, False:0},
    #进出考核大站时,文档要求Int，ODOO提供Boolean
    ('inOrOutBigStation', 'big_station'): {True: 1, False:0},
    #超速阈值,不在调度参数表，在通用设置表
    ('overSpeedThreshold', 'speed_threshold'): None,
    #连续超速时长,不在调度参数表，在通用设置表
    ('continuousOverTime', 'continuous_overspeed_length'): None,
    #连续离线时长,不在调度参数表，在通用设置表
    ('continuousLeavinglineTime', 'continuous_offline_length'): None,
    #长时间停车时长,不在调度参数表，在通用设置表
    ('longTimeStopTime', 'long_time_to_stay_long'): None,
    #长时间停车重发间隔,不在调度参数表，在通用设置表
    ('longTimeStopInterval', 'retransmission_interval'): None,
    #满载率,不在调度参数表，在通用设置表
    ('fullLoadRate', 'passenger_full_load_rate'): None,
    #设备损坏重发间隔,不在调度参数表，在通用设置表
    ('antennaDamageInterval', 'antenna_anomaly_repeat_interval'): None,
    #车到站点未开车门
    ('openCloseDoor0', 'open_the_door'): {True: 1, False:0},
    #车行走中未关车门
    ('openCloseDoor1', 'not_closed_the_door'): {True: 1, False:0},
    #车未关车门离站
    ('openCloseDoor2', 'out_not_closed_the_door'): {True: 1, False:0},
    #有效签点数,不在调度参数表，在通用设置表
    ('dispatchStationLimit', 'number_of_signatures'): None,
}

#人员-IC卡管理 无对应表
# pub_hr_iccardmap
pub_hr_iccardmap = {
    ('id', 'id'): None,
    ('name', None): None,
    ('codeValue', None): None,
}

#运营计划峰值段 无对应表 （sheduleplan_toup，sheduleplan_todown）
# op_planparam
op_planparam = {
    ('id', 'id'): None,
    #计划类型
    ('linePlanId', None): None,
    #参数标志long
    ('flagId', None): None,
    #参数标志String
    ('flagName', None): None,
    #开始时间Date
    ('startTime', None): None,
    #结束时间Date
    ('endTime', None): None,
    #上行间隔1 int
    ('level1', None): None,
    #上行间隔2 int
    ('level2', None): None,
    #上行间隔3 int
    ('level3', None): None,
    #上行间隔4 int
    ('level4', None): None,
    #上行间隔5 int 0:上行，1：下行，2：默认
    ('level5', None): None,
    #时长 int
    ('runTime', None): None,
    #方向 int
    ('direction', None): None,
    #备注 String
    ('remark', None): None,
    #int 无描述
    ('planCount', None): None,
    #int 无描述
    ('avgRestTime', None): None,
    #int 无描述
    ('maxRestTime', None): None,
    #int 无描述
    ('minRestTime', None): None,
}
#1.3.12	控制台
# op_controlline -- dispatch.control.desktop.component
op_controlline = {
    #主键ID
    #调度台id  long
    ('controlsId', 'id'): None,
    #线路id  long
    ('lineId', 'line_id'): None,
    #备注 String
    ('remark', None): None,
    #显示顺序 String
    ('showOrder', None): None,
    #String 没有描述
    ('lineName', None): None,
    #设备号 long
    ('onBoardId', None): None,
}
#1.3.13	司机手动命令，无对应表
# op_commandtext
op_commandtext = {
    ('id', 'id'): None,
    #long 无描述
    ('priorityId', None): None,
    #命令名称String
    ('name', None): None,
    #命令编号 int
    ('eventId', None): None,
    #命令类型int
    ('commandType', None): None,
    #String 无描述
    ('commandTypeName', None): None,
}

#1.3.14	调度计划 无对应表
# op_dispatchplan
op_dispatchplan = {}

#1.3.15	车辆资源 无对应表
# op_busresource
op_busresource = {}

#1.3.16	出勤司机 无对应表
# op_attendance
op_attendance = {}

#1.3.17	出勤乘务员 无对应表
# op_trainattendance
op_trainattendance = {}

origin_data = {
    #线路基础数据
    'route_manage.route_manage': op_line,
    #站台基础数据
    'opertation_resources_station': op_stationblock,
    #车辆基础数据
    'fleet.vehicle': tjs_car,
    #人员基础数据
    'hr.employee': hr_employee,
    #线路计划基础数据
    'scheduleplan.excutetable': op_lineplan,
    #调度参数基础数据
    'res.company': op_param,
}

def dict_transfer(table, data):
    """
    对接数据转换
    :param table: 表名
    :param data: 同步数据
    :return: 
    """
    if origin_data.get(table):
        table_data = origin_data[table]
        new_data = {}
        if isinstance(data, dict):
            for key in data.keys():
                for k, v in table_data.iteritems():
                    if not k[1]:
                        continue
                    if key == k[1]:
                        if v:
                            value = v[data[key]]
                        else:
                            value = data[key]
                        new_data.update({k[0]: value})
            _logger.info('Table: %s, origin Data: %s', table, data)
            _logger.info('Table: %s, Prepare New Data: %s', table, new_data)
            return new_data