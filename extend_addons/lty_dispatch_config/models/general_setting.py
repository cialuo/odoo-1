#-*- coding: utf8 -*-

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    #构成串车标准
    string_car_standard = fields.Integer(default=1)

    #发车间隔参考值
    departure_interval_time = fields.Integer(default=1)

    #小于标准值
    less_departure_interval_time = fields.Integer(defaule=1)

    #大于标准值
    more_departure_interval_time = fields.Integer(defaule=1)

    #两车距离时间差等于或大于(m)
    jet_lag = fields.Integer(defaule=30)

    #串车时提示双方司机
    is_prompt_the_driver = fields.Boolean(defaule=False)

    #串车时提示调度员
    is_prompt_dispatcher = fields.Boolean(defaule=False)

    # 大间隔时提示双方司机
    is_interval_prompt_the_driver = fields.Boolean(defaule=False)

    # 大间隔时提示调度员
    is_interval_prompt_dispatcher = fields.Boolean(defaule=False)

    #司机请假
    driver_leave = fields.Boolean(defaule=False)

    #车辆故障
    vehicle_failure = fields.Boolean(defaule=False)

    #道路堵塞
    road_blockage = fields.Boolean(defaule=False)

    #站点客流过大
    site_traffic_is_too_large = fields.Boolean(defaule=False)

    #超速阈值
    speed_threshold = fields.Integer()

    #连续超速时长
    continuous_overspeed_length = fields.Integer()

    #连续离线时长
    continuous_offline_length = fields.Integer()

    #长时间停车时长
    long_time_to_stay_long = fields.Integer()

    #长时间停车重发间隔
    retransmission_interval = fields.Integer()

    #客流满载率
    passenger_full_load_rate = fields.Integer()

    #天线异常重复间隔
    antenna_anomaly_repeat_interval = fields.Integer()

    #自动同步车辆线路
    is_automatically_synchronize_lines = fields.Boolean(defaule=False)

    # 自动同步车辆线路
    is_automatically_synchronize_operational_status = fields.Boolean(defaule=False)

    #包车限速值
    chart_speed_limit = fields.Integer()

    #非运营限速值
    operational_speed_limit = fields.Integer()

    #是否允许 （发送计划到调度屏）
    is_send_the_plan = fields.Boolean(default=False)

    #提前发送计划时间（分）
    send_time_in_advance = fields.Integer()

    #计划超时判断
    plan_timeout_judgment = fields.Integer()

    #计划执行方式
    plan_execution_mode = fields.Selection([('earliest','earliest'),('recent','recent')],default='earliest')

    #出场带走计划的范围 - 最小
    played_away_min = fields.Integer()

    #出场带走计划的范围 - 最大
    played_away_max = fields.Integer()

    #进站检测计划的范围 - 最小
    in_station_min = fields.Integer()

    #进站检测计划的范围 - 最大
    in_station_max = fields.Integer()

    # 驾驶员晚点预留
    driver_reserved_later = fields.Integer()

    #签到时更换司机
    is_check_replacement_driver = fields.Boolean(default=False)

    #末班车计划检查
    is_last_train_plan_check = fields.Boolean(default=False)

    #有效进出场判断
    effective_access = fields.Integer()

    #每次进场排班计划趟次
    plan_the_trip = fields.Integer()

    #有效进出签点数
    number_of_signatures = fields.Integer()

    #提前发车判断
    ahead_of_departure_to_determine = fields.Integer()

    #缓后发车判断
    slow_after_the_start_to_determine = fields.Integer()

    #车型类型
    vehicle_model_type = fields.Selection([('singleModel','singleModel'),('doubleModels','doubleModels')],default='singleModel')

    #绿色
    green_number = fields.Integer()

    #黄色 - 大于
    yellow_more_number = fields.Integer()

    #黄色 - 小于
    yellow_less_number = fields.Integer()

    #鲜红色 - 大于
    red_more_number = fields.Integer()

    #鲜红色 - 小于
    red_less_number = fields.Integer()

    #深红色 - 大于
    dark_red_more_number = fields.Integer()

    #深红色 - 小于
    dark_red_less_number = fields.Integer()

    # 字体颜色 绿色 - 大于
    green_font_color_more = fields.Integer()

    # 字体颜色 绿色 - 小于
    green_font_color_less = fields.Integer()

    # 字体颜色 黄色 - 大于
    yellow_font_color_more = fields.Integer()

    # 字体颜色 黄色 - 小于
    yellow_font_color_less = fields.Integer()

    # 字体颜色 鲜红色 - 大于
    red_font_color_more = fields.Integer()

    # 字体颜色 鲜红色 - 小于
    red_font_color_less = fields.Integer()

    # 字体颜色 深红色 - 大于
    dark_red_font_color_more = fields.Integer()

    # 字体颜色 深红色 - 小于
    dark_red_font_color_less = fields.Integer()
	
    #计划超时隐藏时间
    plan_hidden_time = fields.Integer()

class General_setting(models.TransientModel):
    _name = 'general.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)

    #构成串车标准
    string_car_standard = fields.Integer(related='company_id.string_car_standard')

    # 发车间隔参考值
    departure_interval_time = fields.Integer(related='company_id.departure_interval_time')

    # 小于标准值
    less_departure_interval_time = fields.Integer(related='company_id.less_departure_interval_time')

    # 大于标准值
    more_departure_interval_time = fields.Integer(related='company_id.more_departure_interval_time')

    # 两车距离时间差等于或大于(m)
    jet_lag = fields.Integer(related='company_id.jet_lag')

    # 串车时提示双方司机
    is_prompt_the_driver = fields.Boolean(related='company_id.is_prompt_the_driver')

    # 串车时提示调度员
    is_prompt_dispatcher = fields.Boolean(related='company_id.is_prompt_dispatcher')

    # 大间隔时提示双方司机
    is_interval_prompt_the_driver = fields.Boolean(related='company_id.is_interval_prompt_the_driver')

    # 大间隔时提示调度员
    is_interval_prompt_dispatcher = fields.Boolean(related='company_id.is_interval_prompt_dispatcher')

    # 司机请假
    driver_leave = fields.Boolean(related='company_id.driver_leave')

    # 车辆故障
    vehicle_failure = fields.Boolean(related='company_id.vehicle_failure')

    # 道路堵塞
    road_blockage = fields.Boolean(related='company_id.road_blockage')

    # 站点客流过大
    site_traffic_is_too_large = fields.Boolean(related='company_id.site_traffic_is_too_large')

    # 超速阈值
    speed_threshold = fields.Integer(related='company_id.speed_threshold')

    # 连续超速时长
    continuous_overspeed_length = fields.Integer(related='company_id.continuous_overspeed_length')

    # 连续离线时长
    continuous_offline_length = fields.Integer(related='company_id.continuous_offline_length')

    # 长时间停车时长
    long_time_to_stay_long = fields.Integer(related='company_id.long_time_to_stay_long')

    # 长时间停车重发间隔
    retransmission_interval = fields.Integer(related='company_id.retransmission_interval')

    # 客流满载率
    passenger_full_load_rate = fields.Integer(related='company_id.passenger_full_load_rate')

    # 天线异常重复间隔
    antenna_anomaly_repeat_interval = fields.Integer(related='company_id.antenna_anomaly_repeat_interval')

    # 自动同步车辆线路
    is_automatically_synchronize_lines = fields.Boolean(related='company_id.is_automatically_synchronize_lines')

    # 自动同步车辆线路
    is_automatically_synchronize_operational_status = fields.Boolean(related='company_id.is_automatically_synchronize_operational_status')

    # 包车限速值
    chart_speed_limit = fields.Integer(related='company_id.chart_speed_limit')

    # 非运营限速值
    operational_speed_limit = fields.Integer(related='company_id.operational_speed_limit')

    # 是否允许 （发送计划到调度屏）
    is_send_the_plan = fields.Boolean(related='company_id.is_send_the_plan')

    # 提前发送计划时间（分）
    send_time_in_advance = fields.Integer(related='company_id.send_time_in_advance')

    # 计划超时判断
    plan_timeout_judgment = fields.Integer(related='company_id.plan_timeout_judgment')

    # 计划执行方式
    plan_execution_mode = fields.Selection([('earliest', 'earliest'), ('recent', 'recent')],related='company_id.plan_execution_mode')

    # 出场带走计划的范围 - 最小
    played_away_min = fields.Integer(related='company_id.played_away_min')

    # 出场带走计划的范围 - 最大
    played_away_max = fields.Integer(related='company_id.played_away_max')

    # 进站检测计划的范围 - 最小
    in_station_min = fields.Integer(related='company_id.in_station_min')

    # 进站检测计划的范围 - 最大
    in_station_max = fields.Integer(related='company_id.in_station_max')

    # 驾驶员晚点预留
    driver_reserved_later = fields.Integer(related='company_id.driver_reserved_later')

    # 签到时更换司机
    is_check_replacement_driver = fields.Boolean(related='company_id.is_check_replacement_driver')

    # 末班车计划检查
    is_last_train_plan_check = fields.Boolean(related='company_id.is_last_train_plan_check')

    # 有效进出场判断
    effective_access = fields.Integer(related='company_id.effective_access')

    # 每次进场排班计划趟次
    plan_the_trip = fields.Integer(related='company_id.plan_the_trip')

    # 有效进出签点数
    number_of_signatures = fields.Integer(related='company_id.number_of_signatures')

    # 提前发车判断
    ahead_of_departure_to_determine = fields.Integer(related='company_id.ahead_of_departure_to_determine')

    # 缓后发车判断
    slow_after_the_start_to_determine = fields.Integer(related='company_id.slow_after_the_start_to_determine')

    # 车型类型
    vehicle_model_type = fields.Selection([('singleModel', 'singleModel'), ('doubleModels', 'doubleModels')],
                                          related='company_id.vehicle_model_type')
    # 绿色
    green_number = fields.Integer(related='company_id.green_number')

    # 黄色 - 大于
    yellow_more_number = fields.Integer(related='company_id.yellow_more_number')

    # 黄色 - 小于
    yellow_less_number = fields.Integer(related='company_id.yellow_less_number')

    # 鲜红色 - 大于
    red_more_number = fields.Integer(related='company_id.red_more_number')

    # 鲜红色 - 小于
    red_less_number = fields.Integer(related='company_id.red_less_number')

    # 深红色 - 大于
    dark_red_more_number = fields.Integer(related='company_id.dark_red_more_number')

    # 深红色 - 小于
    dark_red_less_number = fields.Integer(related='company_id.dark_red_less_number')

    # 字体颜色 绿色 - 大于
    green_font_color_more = fields.Integer(related='company_id.green_font_color_more')

    # 字体颜色 绿色 - 小于
    green_font_color_less = fields.Integer(related='company_id.green_font_color_less')

    # 字体颜色 黄色 - 大于
    yellow_font_color_more = fields.Integer(related='company_id.yellow_font_color_more')

    # 字体颜色 黄色 - 小于
    yellow_font_color_less = fields.Integer(related='company_id.yellow_font_color_less')

    # 字体颜色 鲜红色 - 大于
    red_font_color_more = fields.Integer(related='company_id.red_font_color_more')

    # 字体颜色 鲜红色 - 小于
    red_font_color_less = fields.Integer(related='company_id.red_font_color_less')

    # 字体颜色 深红色 - 大于
    dark_red_font_color_more = fields.Integer(related='company_id.dark_red_font_color_more')

    # 字体颜色 深红色 - 小于
    dark_red_font_color_less = fields.Integer(related='company_id.dark_red_font_color_less')
	
    #计划超时隐藏时间
    plan_hidden_time = fields.Datetime(related='company_id.plan_hidden_time')

    @api.multi
    def execute(self):
        res = super(General_setting, self).execute()
        res = self.env['ir.actions.act_window'].for_xml_id('lty_dispatch_config', 'action_general_config_settings')
        return res