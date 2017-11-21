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
    #线路类型，（1：单向环线；2：双向环线；3：双向线路）
    ('lineTypeId', 'loop_type'): {'single_loop': 1,'double_loop': 2, 'double_line': 3},
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
    #票价
    ('ticketPrice', 'ticket_price'): None,
    #线路开通日期
    ('startDate', 'start_date'): None,
    #线路停运日期
    ('endDate', 'end_date'): None,
    #是否人工售票，（0：非人工；1：人工售票）
    ('isArtificialTicket', 'is_artificial_ticket'): {True: 1, False:0},
    #是否显示线路辅助点，无对应字段（0：不显示；1：显示）,默认传值：0
    ('isShowPoint', None): None,
    #是否显示站点名，无对应字段（0：不显示；1：显示）,默认传值：0
    ('isShowStationName', None): None,
	#公司
    ('companyId', 'company_id'): None,
    #以下三个字段文档未描述
    # 'lineStart': '',
    # 'lineEnd': '',
    # 'companyId': '',
}

#站台基础数据
# op_stationblock opertation_resources_station
op_stationblock = {
    ('id', 'id'): None,
    #站台编码
    ('stationId', 'code'): None,
    #站台名称
    ('stationName', 'name'): None,
    #地址
    ('address', 'address'): None,
    #附近
    ('nearby', 'nearby'): None,
    #经度
    ('longitude', 'longitude'): None,
    #纬度
    ('latitude', 'latitude'): None,
}
#站点基础数据 对应上下行站台两张表，会有重复数据库ID
# op_station -- opertation_resources_station_platform
op_station = {
    ('id', 'id'): None,
    #线路编码int 后台获取route_id.gprs_id
    ('gprsId', None): None,
    #站点名称string，后台获取station_id.name
    ('stationName', None): None,
    #站点方案Id int ，not found
    ('opStationMainId', 'id'): None,
    #线路Id int，route_id
    ('lineId', 'route_id'): None,
    #站序 int ，
    ('orderNo', 'sequence'): None,
    #方向 0:上行，1：下行
    ('direction', 'direction'): {'up': 0, 'down': 1},
    #站台id int
    ('blockId', 'station_id'): None,
    #距起点站距离 float,notfound
    ('byStartDistance', 'by_start_distance'): None,
    #进站经度 float,后台获取 station_id.entrance_longitude
    ('longitude', None): None,
    #进站纬度 float 后台获取 station_id.entrance_latitude
    ('latitude', None): None,
    #进站角度 int  后台获取 station_id.entrance_azimuth
    ('angle', None): None,
    #出站经度 float 后台获取 station_id.exit_longitude
    ('longitudeOut', None): None,
    #出站纬度 float 后台获取 station_id.exit_latitude
    ('latitudeOut', None): None,
    #出站角度 int 后台获取 station_id.exit_azimuth
    ('angleOut', None): None,
    #距下一站时间 ， not found
    ('toNextTime', 'to_next_time'): None,

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
    #设备号
    ('onBoardId', 'on_boardid'): None,
    #车辆编号
    ('carNum', 'inner_code'): None,
    #车辆牌照
    ('licensePlate', 'license_plate'): None,
    #发动机号,计算字段后台获取 model_id.engine_no
    ('engineNo', 'engine_no'): None,
    #是否营运
    ('ifService', 'vehicle_life_state'): {'operation_period': 0, 'invest_period': 1, 'scrap_period': 1},
    #载客数，计算字段后台获取 model_id.ride_number
    ('Zkrs', 'ride_number'): None,
    #座位数，计算字段后台获取 model_id.seats_ext
    ('Zws', 'seats_ext'): None,
    #总运营公里,计算字段后台获取,total_odometer
    ('Zyygl', 'total_odometer'): None,
    #车辆类型,
    ('typeId', 'model_id'): None,
    #客门形式ID，无在对应字段；（1:1前2后；2:2前2后；3:2前1后；4:2前2后），2,4重复，默认传值：1
    ('doorTypeId', None): None,
    #部门ID
    ('departmentId', 'company_id'): None,

}

#人员基础数据
# hr_employee
hr_employee = {
    ('id', 'id'): None,
    #用户ID，
    ('userId', 'user_id'): None,
    #用户名称
    ('trueName', 'name'): None,
    #工号
    ('serils', 'jobnumber'): None,
    #岗位ID, 后台获取  1019 司机 1020 乘务员  1021其他
    ('sysPostId', None): None,
    #IC卡号
    ('ICCardNoId', 'iccard'): None,
    #身份证
    ('sfz', 'id_card'): None,
    #删除状态
    ('delState', 'active'): {True:0,False:1},
    #部门ID
    ('sysDepartmentId', 'department_id'): None,

}

#线路计划基础数据
# op_linePlan -- scheduleplan.schedulrule
op_lineplan = {
    ('id', 'id'): None,
    #编号，无对应字段,传ID
    ('serialNumber', 'id'): None,
    #线路 ID
    ('lineId', 'line_id'): None,
    #线路编码，无对应字段,后台取值line_id.gprs_id
    ('gprsID', 'gprs_id'): None,
    # 调车方式
    ('runTypeId', 'schedule_method'): {'singleway': 1,'dubleway': 2},
    #调度类型编码,无对应字段，后台取值，line_id.schedule_type
    ('dispatchModeId', 'schedule_type'): {'flexible_scheduling': 1003, 'planning_scheduling': 1004, 'hybrid_scheduling': 2027},
    #计划名称
    ('planName', 'name'): None,
    #上行里程
    ('runKmU', 'run_km_u'): None,
    #下行里程
    ('runKmD', 'run_km_d'): None,
    #上行首班时间 Datetime
    ('firstTime', 'upfirsttime'): None,
    #上行末班时间 Datetime
    ('lastTime', 'uplasttime'): None,
    # #计划趟次,无对应字段
    # ('planCount', None): None,
    #下行首班时间 Datetime
    ('firstTimeD', 'downfirsttime'): None,
    #下行末班时间 Datetime
    ('lastTimeD', 'downlasttime'): None,
    #开始计划 Datetime,无对应字段
    ('startPlanTime', 'start_plan_time'): None,
    #创建日期
    ('createDate', 'create_date'): None,
    #主场站ID
    ('mainFieldId', 'main_field_id'): None,
    #副场站ID
    ('viceFieldId', 'vice_field_id'): None,

}

#大站设置
# op_planstationbigmain  scheduleplan.bigsitesetdown scheduleplan.bigsitesetup
op_planstationbigmain = {
    #id string,id+ up /down
    ('id', 'id'): None,
    #运营计划ID int
    ('linePlanId', 'rule_id'): None,
    #方案站点ID int not found  线路ID ，后台获取
    ('opStationMainId', 'line_id'): None,
    #站点ID int
    ('stationId', 'site_id'): None,
    #站点名称,后台获取 site_id.name
    ('stationName', 'station_name'): None,
    # #距起点站距离float,not found
    # ('byStartDistance', None): None,
    #是否大站考核,0:否，1：是
    ('isCheck', 'needchecking'): {True: 1,False:0},
    #是否签点,0：否，1：是
    ('isDispatchStation', 'needsign'): {True: 1,False:0},
    #允许快几分钟 int
    ('fastTime', 'fastthen'): None,
    #允许慢几分钟 int
    ('slowTime', 'slowthen'): None,
    #方向 int  0
    ('direction', 'direction'): {'up': 0,'down':1},
    #距上一站时间（低峰）
    ('byLastStationLow', 'tolastsit_low'): None,
    #距上一站时间（平峰）
    ('byLastStationNormal', 'tolastsit_flat'): None,
    #距上一站时间（高峰）
    ('byLastStationHigh', 'tolastsit_peak'): None,
    #站点序号 int 9-13增加
    ('orderNo', 'site_seq'): None,
    # #峰段标志ID 1001:低峰；1002：平峰；1003：高峰 not found
    # ('flagId', None): None,
    # #峰段标志名称 string not found
    # ('flagName', None): None,
    # #到下站考核时间点 string not found
    # ('checkTime', None): None,
}

#调度线路基础数据
# op_DspLine opertation_resources_vehicle_yard
op_dspLine = {
    ('id', 'id'): None,
    #名称 int
    ('lineId', 'name'): None,
    # #调度服务Id int not found 不传
    # ('dspId', None): None,
    #线路名称 string,后台获取 route_id.name
    ('lineName', 'route_name'): None,
    #方向int  必填;0：上行；1：下行
    ('direction', 'direction'): {'up': 0,'down': 1, 'one_way': 0},
    #车场编码long 必填;
    ('fieldNo', 'code'): None,
    #车场名称String
    ('fieldName', 'yard_name'): None,
    #屏幕1 int 后台获取编码
    ('screen1', 'screen1'): None,
    #屏幕2 int  后台获取编码
    ('screen2', 'screen2'): None,

}


#调度参数基础数据
#对应两个表  dispatch.config.settings   general.config.settings
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
    #('planViewRange', None): None,
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
    ('driverSingin', 'driver_goes_to_work'): {True: 1, False:0},
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
    #计划陷藏时间，在通用设置表
    ('planViewRange', 'plan_hidden_time'): None,		
}

#人员-IC卡管理
# pub_hr_iccardmap  employees.iccards
pub_hr_iccardmap = {
    ('id', 'id'): None,
    #传 员工工号
    ('name', 'employee_jobnumber'): None,
    # IC卡名称，也为 物理卡号
    ('codeValue', 'cardsn'): None,
}

#运营计划峰值段  （scheduleplan.toup，scheduleplan.todown）
# op_planparam
op_planparam = {
    #上行 id 后缀+0, 下行 id后缀+1
    ('id', 'id'): None,
    #计划类型
    ('linePlanId', 'rule_id'): None,
    #参数标志long
    ('flagId', 'mark'): {'peak': 3,'flat': 2,'low': 1, False:0},
    #参数标志String
    ('flagName', 'mark'): None,
    #开始时间Date
    ('startTime', 'starttime'): None,
    #结束时间Date
    ('endTime', 'endtime'): None,
    #上行间隔1 int not found
    ('level1', 'interval'): None,
    # #上行间隔2 int not found
    # ('level2', None): None,
    # #上行间隔3 int not found
    # ('level3', None): None,
    # #上行间隔4 int not found
    # ('level4', None): None,
    # #上行间隔5 int not found
    # ('level5', None): None,
    #时长 int
    ('runTime', 'worktimelength'): None,
    #方向 int not found 0:上行，1：下行，2：默认
    ('direction', 'direction'): {'up': 0,'down': 1},
    # #备注 String not found
    # ('remark', None): None,
    # #int 无描述不传
    # ('planCount', None): None,
    # #int 无描述不传
    # ('avgRestTime', None): None,
    # #int 无描述不传
    # ('maxRestTime', None): None,
    # #int 无描述不传
    # ('minRestTime', None): None,
}
#1.3.12	控制台
# op_controlline -- dispatch.control.desktop.component
op_controlline = {
    #主键ID
    ('id', 'id'): None,
    #调度台id  long
    ('controlsId', 'desktop_id'): None,
    #线路id  long
    ('lineId', 'line_id'): None,
    #备注 String
    ('remark', 'remark'): None,
    #显示顺序 String
    ('showOrder', 'show_order'): None,
    #String 没有描述，后台获取line_name
    ('lineName', None): None,
    #设备号 long
    ('onBoardId', 'on_bord_id'): None,
}
#1.3.13	司机手动命令，
# op_commandtext  dispatch.driver.command
op_commandtext = {
    ('id', 'id'): None,
    #long 无描述
    ('priorityId', 'proiority'): None,
    #命令名称String
    ('name', 'name'): None,
    #命令编号 int
    ('eventId', 'event_code'): None,
    #命令类型int
    ('commandType', 'command_type_id'): None,
    #String 无描述 后台获取
    ('commandTypeName', 'command_type_name'): None,
}

#1.3.14	调度计划
# op_dispatchplan -- scheduleplan.execupplanitem,scheduleplan.execdownplanitem
op_dispatchplan = {
    ('id', 'id'): None,
    #线路Id  主表 行车作业时间表的线路ID
    ('lineId', 'main_line_id'): None,
    #线路名称 String 后台获取传值
    ('lineName', None): None,
    #线路gprsid  int后台获取传值
    ('gprsId', None): None,
    #运行线路编码 int  当前线路ID
    ('runGprsId', 'run_gprsid'): None,
    #车辆编号Stirng not found后台获取传值
    ('selfId', None): None,
    #设备号int not found后台获取传值
    ('onBoardId', None): None,
    #驾驶员工号String not found后台获取传值
    ('workerId', None): None,
    #驾驶员姓名 string 后台取值
    ('driverName', None): None,
    #发车方向int not found后台获取传值
    ('direction', None): None,
    #计划发车时间
    ('planRunTime', 'starttime'): None,
    #计划到达时间，
    ('planReachTime', 'arrivetime'): None,
    #计划时长
    ('planDuration', 'timelenght'): None,
    #计划里程
    ('planKm', 'mileage'): None,
    #乘务员工号，后台获取
    ('trainId', None): None,
    # 乘务员姓名，后台获取
    ('trainName', None): None,
    #工作日期 后台获取 计划 执行时间
    ('workDate', 'work_date'): None,
    #行车规则ID 后台获取
    ('linePlanId', 'rule_id'): None,
    #
}

#1.3.15	车辆资源
# op_busresource -- scheduleplan.vehicleresource
op_busresource = {
    ('id', 'id'): None,
    #线路id not found 后台获取
    ('lineId', None): None,
    #线路NameString not found 后台获取
    ('lineName', None): None,
    #线路编码 int
    ('gprsId', None): None,
    #设备编号int not found 后台获取
    ('onBoardId', None): None,
    #车号 not found 后台获取
    ('carNum', None): None,
    #台次 add
    ('orderNo', 'arrangenumber'): None,
    #车辆状态 add
    ('carStateId', 'workstatus'): {'operation': 1001, 'flexible': 2008},
    #方向 add
    ('direction', 'direction'): {'up': 0, 'down': 1},
    #工作日期date 后台获取，
    ('workDate', 'work_date'): None,
}

#1.3.16	出勤司机
# op_attendance -- scheduleplan.motorcyclists
op_attendance = {
    ('id', 'id'): None,
    #线路ID long, notfound，计划中获取
    ('lineId', None): None,
    #线路名称String,notfound，计划中获取
    ('lineName', None): None,
    #调度计划ID long notfound
    ('dispatchPlanId', 'execplan_id'): None,
    #车辆编号 String 车辆自编号，后台获取
    ('selfId', 'self_id'): None,
    #设备编号 int 车辆获取
    ('onBoardId', 'on_boardid'): None,
    #线路编码int,notfound，计划中获取
    ('gprsId', None): None,
    #台次int
    ('orderNo', 'order_numer'): None,
    #计划签到时间
    ('onWorkTime', 'checkintime'): None,
    #实际签到时间,
    ('conWorkTime', 'con_work_time'): None,
    #实际签到车辆,
    ('onWorkBus', 'on_work_bus'): None,
    #实际签退时间date,
    ('coffWorkTime', 'c_off_work_time'): None,
    #实际签退车辆
    ('offWorkBus', 'off_work_bus'): None,
    #工号String
    ('workerId', 'employee_sn'): None,
    #姓名String,notfound，员工中获取
    ('driverName', None): None,
    #执行日期date 后台获取
    ('workDate', 'work_date'): None,
    #备注String
    ('remark', 'remark'): None,
    #计划发车时间
    ('planRunTime', 'plan_run_time'): None,
    #时间发车时间date
    ('planReachTime', 'plan_reach_time'): None,
    #上班时间
    ('workTime', 'checkintime'): None,
    #计划时间date
    ('planTime', 'plan_time'): None,
    #员工类型int 1019:司机 1020:售票员
    ('workerType', 'title'): {'driver': 1019, 'steward': 1020},

}

#1.3.17	出勤乘务员
# op_trainattendance -- scheduleplan.motorcyclists
op_trainattendance = {
    ('id', 'id'): None,
    # 线路ID long, notfound，计划中获取
    ('lineId', None): None,
    # 线路名称String,notfound，计划中获取
    ('lineName', None): None,
    # 调度计划ID long
    ('dispatchPlanId', 'execplan_id'): None,
    # 车辆编号 String
    ('selfId', 'self_id'): None,
    # 设备编号 int,
    ('onBoardId', 'on_boardid'): None,
    # 线路编码int,notfound，计划中获取
    ('gprsId', None): None,
    # 台次int,
    ('orderNo', 'order_numer'): None,
    # 计划签到时间, 等于 上班时间
    ('onWorkTime', 'checkintime'): None,
    # 实际签到时间,
    ('conWorkTime', 'con_work_time'): None,
    # 实际签到车辆,
    ('onWorkBus', 'on_work_bus'): None,
    # 实际签退时间date,
    ('coffWorkTime', 'c_off_work_time'): None,
    #清除签退时间boolean,notfound
    ('isClearCoffWorkTime', None): None,
    # 实际签退车辆,
    ('offWorkBus', 'off_work_bus'): None,
    # 工号String
    ('trainId', 'employee_sn'): None,
    # 姓名String,notfound，员工中获取
    ('trainName', None): None,
    #执行日期date 后台获取
    ('workDate', 'work_date'): None,
    # 备注String,
    ('remark', 'remark'): None,
    # 计划发车时间,
    ('planRunTime', 'plan_run_time'): None,
    # 时间发车时间date,
    ('planReachTime', 'plan_reach_time'): None,
    # 上班时间
    ('workTime', 'checkintime'): None,
    # 计划时间date,
    ('planTime', 'plan_time'): None,
    # 员工类型int 1019:司机 1020:售票员
    ('type', 'title'): {'driver': 1019, 'steward': 1020},
}
#用户表
#sys_user -- res.users
sys_user = {
    ('id', 'id'): None,
    ('UserName', 'name'): None,
    ('UserPwd', 'password'): None,
    ('delState', 'active'): {True:0,False:1}
}
#运营理程 非运营理程表
#operate+nonOperate -- vehicleusage.driverecords
operate_nonOperate = {
	#数据库id
    ('id', 'restful_key_id'): None,
	#线路id  运营+非运营
    ('lineId', 'route_id'): None,
	#司机ID 运营+非运营
    ('workerId', None): None,
	#车辆设备号 运营+非运营
    ('onboardId', 'inner_code'): None,
	#方向
    ('direction', 'direction'): None,
	#gps理程
    ('gpsKm', 'GPSmileage'): None,
	#是否异常
    ('isExcept', 'abnormal'): None,
	#车型
    ('busType', None): None,
	#增加原因
    ('addReasonId', None): None,
	#计划类型ID
    ('planTypeId', None): None,
	#工作日期
    ('workDate', 'date'): None,
	#Remark ???
    ('remark', None): None,
	#异常时间
    ('exceptTime', None): None,
	#异常站点
    ('exceptStation', None): None,
	#异常原因ID
    ('exceptReasonId', None): None,
	#实际发车时间
    #('exceptReasonId', 'realitydepart'): None,
	#实际到达时间
    ('realReachTime', 'realityarrive'): None,
	#司机姓名
    ('driverName', 'driver_name'): None,
	#planCount？？？
    ('planCount', None): None,
	#invalidCount ??
    ('invalidCount', None): None,
	#planStateId ??
    ('planStateId', None): None,	
	#以下为odoo所有界面的字段传输信息
	#是否补录
    ('is_add', 'is_add'): None,	
	#类型
    ('drivetype', 'drivetype'): None,	
	#公司
    ('company_id', 'company_id'): None,		
	#线路
    ('route_id', 'route_id'): None,			
	#方向
    ('direction', 'direction'): None,		
	#执行日期
    ('date', 'date'): None,		
	#计划时间
    ('date_plan', 'date_plan'): None,			
	#实际发车时间
    ('realitydepart', 'realitydepart'): None,		
	#计划状态
    ('state_plan', 'state_plan'): None,		
	#车辆编号
    ('vehicle_id', 'vehicle_id'): None,		
	#司机工号
    ('driver_id', 'driver_id'): None,	
	#司机姓名
    ('driver_name', 'driver_name'): None,	
	#计划到达时间
    ('planarrive', 'planarrive'): None,	
	#实际到达时间
    ('realityarrive', 'realityarrive'): None,	
	#运营时长
    ('time_operation', 'time_operation'): None,	
	#计划公理数
    ('planmileage', 'planmileage'): None,	
	#GPS公理数
    ('GPSmileage', 'GPSmileage'): None,	
	#运营属性
    ('operation_att', 'operation_att'): None,	
	#异常
    ('abnormal', 'abnormal'): None,		
	#生成日期
    ('gen_date', 'gen_date'): None,	
	#备注
    ('note', 'note'): None,	
	#状态
    ('state', 'state'): None,		
}
#考勤信息表表
#attend -- employee.attencerecords
attend = {
	#   数据库ID
    ('id', 'restful_key_id'): None,
	#   * "线路ID"
    ('lineId', 'line_id'): None,
	#   * "线路名称"  添加到代码里
    ('line', None): None,
	#   * "调度计划ID"
    ('dispatchPlanId', None): None,
	#   * "车辆编号"  添加到代码里
    ('selfId', None): None,
	#   * "设备编号"  添加到代码里
    ('onBoardId', None): None,
	#   * "线路编码"  添加到代码里
    ('gprsId', None): None,
	#   "台次"
    ('orderNo', None): None,
	#   * "计划签到时间"
    ('onWorkTime', None): None,
	#   * "实际签到时间"
    ('conWorkTime', 'checkingin'): None,
	#   "实际签到车辆"
    ('onWorkBus', None): None,
	#   "实际签退时间"
    ('coffWorkTime', 'checkinginout'): None,
	#   "实际签退车辆"
    ('offWorkBus', None): None,
	#   "工号"  添加到代码里
    ('workerId', None): None,
	#   "姓名"  添加到代码里
    ('driver', None): None,
	#   "执行日期"
    ('workDate', 'date'): None,
	#   "备注"
    ('remark', None): None,
	#   "计划发车时间"
    ('planRunTime', None): None,
	#   "实际发车时间"
    ('planReachTime', None): None,
	#   "上班时间"
    ('workTime', None): None,
	#   "计划时间"
    ('planTime', None): None,
	#员工类型//1019 司机  1020 售票员
    ('workerType', 'work_type_id'): None,
	#以下为odoo所有界面的字段传输信息
	#补录
    ('is_add', 'is_add'): None,	
	#公司
    ('company_id', 'company_id'): None,		
	#线路
    ('line_id', 'line_id'): None,			
	#车辆
    ('vehicle_id', 'vehicle_id'): None,			
	#职工
    ('vehicle_id', 'vehicle_id'): None,		
	#员工类型
    ('work_type_id', 'work_type_id'): None,		
	#日期
    ('date', 'date'): None,	
	#签到时间
    ('checkingin', 'checkingin'): None,	
	#签退时间
    ('checkinginout', 'checkinginout'): None,	
	#状态
    ('state', 'state'): None,	
}


origin_data = {
    #线路基础数据
    'route_manage.route_manage': op_line,
    #站台基础数据
    'opertation_resources_station': op_stationblock,
    #站点基础数据
    'opertation_resources_station_platform': op_station,
    #车辆基础数据
    'fleet.vehicle': tjs_car,
    #人员基础数据
    'hr.employee': hr_employee,
    #线路计划基础数据
    'scheduleplan.schedulrule': op_lineplan,
    #大站设置
    'scheduleplan.bigsitesetdown': op_planstationbigmain,
    'scheduleplan.bigsitesetup': op_planstationbigmain,
    #调度线路基础数据 无对应的数据库表
    # op_DspLine opertation_resources_vehicle_yard
    'opertation_yard_lines': op_dspLine,
    #调度参数基础数据
    'dispatch.config.settings': op_param,
    'general.config.settings': op_param,
    #IC卡管理
    'employees.iccards': pub_hr_iccardmap,
    # 运营计划峰值段  （scheduleplan.toup，scheduleplan.todown）
    # op_planparam
    'scheduleplan.toup': op_planparam,
    'scheduleplan.todown': op_planparam,
    #1.3.12	控制台
    # op_controlline -- dispatch.control.desktop.component
    'dispatch.control.desktop.component': op_controlline,
    #1.3.13	司机手动命令，
    # op_commandtext  dispatch.driver.command
    'dispatch.driver.command': op_commandtext,
    # 1.3.14	调度计划
    # op_dispatchplan -- scheduleplan.execupplanitem,scheduleplan.execdownplanitem
    'scheduleplan.execupplanitem': op_dispatchplan,
    'scheduleplan.execdownplanitem': op_dispatchplan,
    #1.3.15	车辆资源
    # op_busresource -- scheduleplan.vehicleresource
    'scheduleplan.vehicleresource': op_busresource,
    #出勤司机
    'scheduleplan.motorcyclists.driver': op_attendance,
    #出勤乘务员
    'scheduleplan.motorcyclists.steward': op_trainattendance,
    #用户表
    'res.users': sys_user,
    #运营里程
    
    'vehicleusage.driverecords': operate_nonOperate,	
    #考勤信息表表
    'employee.attencerecords': attend,		
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
                            if not value:
                                value = 0
                        new_data.update({k[0]: value})
            _logger.info('Table: %s, origin Data: %s', table, data)
            _logger.info('Table: %s, Prepare New Data: %s', table, new_data)
            return new_data