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
route_data = {
    #线路ID
    ('id', 'id'): None,
    #线路编码
    ('gprsId', 'gprsId'): None,
    #线路名称
    ('lineName', 'lineName'): None,
    #线路类型，无对应字段（1：单向环线；2：双向环线；3：双向线路）
    ('lineTypeId', None): None,
    #调车方式
    ('runTypeId', 'runTypeName'): {'single_shunt': 1, 'double_shunt':2},
    #调度类型
    ('dispatchModeId', 'schedule_type'): {'flexible_scheduling': 1003, 'planning_scheduling': 1004, 'hybrid_scheduling': 2027},
    #文档中提供的班制是 001,002,003 不符合文档中提供的类型long
    ('classSystemId', 'classSystemName'): {'one_shift': 1, 'two_shift': 2, 'three_shift': 3},
    #文档提供的类型是Long，只能提供 部门ID
    ('departmentId', 'department_id'): None,
    #是否环线，无对应字段（0：环线；1：非环线）
    ('isRoundLine', None): None,
    #是否夜班线路，无对应字段（0：非夜班；1：夜班线路）
    ('isNight', None): None,
    #是否跨天，无对应字段(0：跨天；1：非跨天)
    ('isCrossDay', None): None,
    #票价，无对应字段
    ('ticketPrice', None): None,
    #线路开通日期，无对应字段
    ('startDate', None): None,
    #线路停运日期，无对应字段
    ('endDate', None): None,
    #是否人工售票，无对应字段（0：非人工；1：人工售票）
    ('isArtificialTicket', None): None,
    #是否显示线路辅助点，无对应字段（0：不显示；1：显示）
    ('isShowPoint', None): None,
    #是否显示站点名，无对应字段（0：不显示；1：显示）
    ('isShowStationName', None): None,
    #以下三个字段文档未描述
    # 'lineStart': '',
    # 'lineEnd': '',
    # 'companyId': '',
}

#站点基础数据 无法对应表
station_data = {
}

#车辆基础数据
fleet_data = {
    ('id', 'id'): None,
    #线路编码，无对应字段
    ('modelArgId', None): None,
    #线路ID
    ('lineId', 'route_id'): None,
    #车辆状态编码,文档中提供的是 001,002,003，004，不符合文档中提供的类型long
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
    #客门形式ID，无在对应字段；（1:1前2后；2:2前2后；3:2前1后；4:2前2后），2,4重复
    ('doorTypeId', None): None,

}

#人员基础数据
employee_data = {
    ('id', 'id'): None,
    #用户编号，无对应字段，ODOO中用户编码为string
    ('userId', None): None,
    #用户名称
    ('userStateName', 'name'): None,
    #手机号码
    ('mobilePhone', 'mobile_phone'): None,
    #邮箱
    ('email', 'work_email'): None,
    #工号
    ('Serils', 'jobnumber'): None,
    #员工类型编码，无对应字段
    ('sysPostId', None): None,
    #IC卡号
    ('ICCardNoId', 'iccard'): None,
    #身份证
    ('sfz', 'id_card'): None,
}

#线路计划基础数据
scheduleplan_data = {
    ('id', 'id'): None,
    #编号，无对应字段
    ('serialNumber', None): None,
    #线路 ID
    ('lineId', 'line_id'): None,
    #线路编码，无对应字段
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

#调度线路基础数据
#无对应的数据库表

#调度参数基础数据
#由于参数在不同的Model定义，只能从res.company取值，则只有 write 接口
config_data = {
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
    ('autoSyncStatus', 'is_automatically_synchronize_operational_status'): None,
    #自动同步车辆路线,文档要求Int，ODOO提供Boolean
    ('autoSyncLine', 'is_automatically_synchronize_lines'): None,
    #向司机发送短消息 车辆超载时,文档要求Int，ODOO提供Boolean
    ('busOverLoading', 'vehicle_overload'): None,
    #发车计划误点时,文档要求Int，ODOO提供Boolean
    ('delayedDeparturePlan', 'plan_to_be_delayed'): None,
    #进出考核大站时,文档要求Int，ODOO提供Boolean
    ('inOrOutBigStation', 'big_station'): None,
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

origin_data = {
    'route_manage.route_manage': route_data,
    'opertation_resources_station': station_data,
    'fleet.vehicle': fleet_data,
    'hr.employee': employee_data,
    'scheduleplan.excutetable': scheduleplan_data,
    'dispatch.config.settings': config_data,
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