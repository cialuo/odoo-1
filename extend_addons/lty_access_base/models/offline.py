# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lineTimeTopic(models.Model):

    _name = 'lty_access_base.line_time_topic'

    _description = 'Line Time Topic'

    _rec_name = 'city_code'

    '''线路分时客流'''

    #城市
    city_code = fields.Char()

    #线路
    route_id = fields.Many2one('route_manage.route_manage')

    #线路方向 1：上行,2：下行,数据类型需要跟调度统一
    line_direction = fields.Integer()

    #时间类型 1：时间,2：日,3：周,4：月,默认为0
    time_type = fields.Integer(default=0)

    #日期类型 1：节假日:2：周末:3：工作日,默认为0
    date_type = fields.Integer(default=0)

    #日期 年月日
    off_date = fields.Char()

    #时间 24小时制
    off_time = fields.Char()

    #预测客流
    prediction_passenger_num = fields.Integer()

    #历史客流
    history_passenger_num = fields.Integer()

    #候车满意度
    waiting_satisfaction = fields.Integer()

    #滞站客流（等车人数）
    stagnant_traffic = fields.Integer()

class stationTimeTopic(models.Model):

    _name = 'lty_access_base.station_time_topic'
    _description = 'Station time topic'
    _rec_name = 'station_name'

    '''站点分时客流'''

    #城市
    city_code = fields.Char()

    #线路
    route_id = fields.Many2one('route_manage.route_manage')

    #线路方向
    line_direction = fields.Integer()

    #日期类型
    date_type = fields.Integer()

    #时间类型
    time_type = fields.Integer()

    #日期
    off_date = fields.Char()

    #时间
    off_time = fields.Char()

    #站点名称
    station_name = fields.Char()

    #站点
    station_main_id = fields.Many2one('platform_manage.platform_manage')

    #客流
    passenger_flow = fields.Integer()

class punctualityDetentionTopic(models.Model):

    _name = 'lty_access_base.punctuality_detention_topic'

    _description = 'Punctuality detention topic'

    _rec_name = 'station_name'

    '''准点与滞站'''

    #城市id
    city_code = fields.Char()

    #线路id
    route_id = fields.Many2one('route_manage.route_manage')

    #线路方向
    line_direction = fields.Integer()

    #时间类型
    time_type = fields.Integer()

    #日期类型
    date_type = fields.Integer()

    #日期
    off_date = fields.Char()

    #时间
    off_time = fields.Char()

    #是否准点
    punctuality_rate = fields.Integer()

    #滞站客流
    stagnant_traffic = fields.Integer()

    #站点名称
    station_name = fields.Char()

    #站点ID
    station_main_id = fields.Many2one('platform_manage.platform_manage')

class passengerSatisfactionTopic(models.Model):

    _name = 'lty_access_base.passenger_satisfaction_topic'

    _description = 'Passenger satisfaction topic'

    _rec_name = 'route_id'

    '''乘客满意度'''

    #城市id
    city_code = fields.Char()

    #线路id
    route_id = fields.Many2one('route_manage.route_manage')

    #线路方向
    line_direction = fields.Integer()

    #时间类型
    time_type = fields.Integer()

    #日期类型
    date_type = fields.Integer()

    #日期
    off_date = fields.Char()

    #时间
    off_time = fields.Char()

    #公交公司ID
    department_id = fields.Char()

    #上车人数
    up_number = fields.Integer()

    #下车人数
    down_number = fields.Integer()

    #平均发车间隔
    average_start_interval = fields.Integer()

    #侯车满意度
    waiting_satisfaction = fields.Integer()

    #舒适满意度
    comfort_satisfaction = fields.Integer()

class serviceSupportCapabilityTopic(models.Model):

    _name = 'lty_access_base.service_support_capability_topic'
    _abstract = 'Service support capability topic'
    _rec_name = 'city_code'

    '''服务保障能力'''

    #城市id
    city_code = fields.Char()

    #线路id
    route_id = fields.Many2one('route_manage.route_manage')

    #线路方向
    line_direction = fields.Integer()

    #时间类型
    time_type = fields.Integer()

    #日期类型
    date_type = fields.Integer()

    #日期
    off_date = fields.Char()

    #时间
    off_time = fields.Char()

    #站点ID
    station_main_id = fields.Many2one('platform_manage.platform_manage')

    #历史客流
    passenger_flow = fields.Integer()

    #公交公司ID
    department_id = fields.Char()

class stationMayArrTimeTopic(models.Model):

    _name = 'lty_access_base.station_may_arr_time_topic'
    _description = 'Station may arrt ime topic'
    _rec_name = 'city_code'

    '''车辆到站预测准点'''

    #设备号
    onboard_id = fields.Char()

    #城市id
    city_code = fields.Char()

    #计划编号
    plan_id = fields.Integer()

    #线路方向
    line_direction = fields.Integer()

    #编码
    gprs_id = fields.Integer()

    #站点id
    station_id = fields.Many2one('platform_manage.platform_manage')

    #预测到站时间
    may_arrival_time = fields.Datetime()

    #站点序号
    station_no = fields.Integer()

class drivingRulesTopic(models.Model):

    _name = 'lty_access_base.driving_rules_topic'
    _description = 'Driving rules topic'
    _rec_name = 'city_code'

    '''行车规则'''

    #城市id
    city_code = fields.Char()

    #线路id
    route_id = fields.Many2one('route_manage.route_manage')

    #线路方向
    line_direction = fields.Integer()

    #公交公司ID
    department_id = fields.Char()

    #日期类型
    date_type = fields.Integer()

    #开始时间
    start_time = fields.Datetime()

    #结束时间
    end_time = fields.Datetime()

    #发车间隔
    departure_interval = fields.Integer()

    #预测车速
    predicted_speed = fields.Integer()

    #运营时长
    operation_duration = fields.Integer()

    #停车时间
    parking_time = fields.Integer()

    #最小配车数
    smallest_bus = fields.Integer()

    #富余车辆
    surplus_bus = fields.Integer()

    #客流采集天数
    passenger_collection_days = fields.Integer()

    #是否跨天
    isInter_day = fields.Integer()

    #标志
    line_signs = fields.Integer()















