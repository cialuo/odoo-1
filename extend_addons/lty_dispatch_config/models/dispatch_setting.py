#-*- coding: utf8 -*-

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    #显示发车异常
    is_show_departure_exception = fields.Boolean(default=False)

    #显示车辆置顶
    is_show_vehicle_top = fields.Boolean(default=False)

    #显示车辆掉线
    is_show_vehicle_dropped = fields.Boolean(default=False)

    #显示设备异常
    is_display_device_exception = fields.Boolean(default=False)

    #显示车辆超速
    is_show_vehicle_speeding = fields.Boolean(default=False)

    #显示车辆离线离开
    is_show_vehicle_offline = fields.Boolean(default=False)

    #显示开关车门
    is_display_switch_door = fields.Boolean(default=False)

    #显示乘客纠纷
    is_show_passenger_disputes = fields.Boolean(default=False)

    #显示计划误点
    is_show_plans_are_delayed = fields.Boolean(default=False)

    #显示疑似抛锚
    is_show_suspected_down = fields.Boolean(default=False)

    #显示超速
    is_show_overspeed = fields.Boolean(default=False)

    #只显示多少时速以上的提示
    speed_limit = fields.Integer()

    #超速时自动弹出视频
    is_speeding_automatically_video = fields.Boolean(default=False)

    #报警时自动弹出视频
    is_alarm_automatically_video = fields.Boolean(default=False)

    #疑似抛锚时自动弹出视频
    is_anchor_automatically_video = fields.Boolean(default=False)

    #同意请求派班
    is_agree_ask = fields.Boolean(default=False)

    #签到立即派班
    is_attendance_ask = fields.Boolean(default=False)

    #不签到不派班
    is_unattendance_ask = fields.Boolean(default=False)

    #是否允许
    is_send_plan_to_vehicle = fields.Boolean(default=False)

    #提前发送时间
    send_plan_advance_time = fields.Integer()

    #车到站点为开车门
    open_the_door = fields.Boolean(default=False)

    #车行走中未关车门
    not_closed_the_door = fields.Boolean(default=False)

    #车未关车门离站
    out_not_closed_the_door = fields.Boolean(default=False)

    #非站点开车门
    non_site_driving_door = fields.Boolean(default=False)

    #取消发车计划
    cancel_departure_plan = fields.Boolean(default=False)

    #司机命令
    driver_command = fields.Boolean(default=False)

    #司机上班签到时
    driver_goes_to_work = fields.Boolean(default=False)

    #司机下班签退时
    driver_checked_out = fields.Boolean(default=False)

    #安排司机短休时
    driver_short_break = fields.Boolean(default=False)

    #进出考核大站时
    big_station = fields.Boolean(default=False)

    #发车计划误点时
    plan_to_be_delayed = fields.Boolean(default=False)

    #车辆超载时
    vehicle_overload = fields.Boolean(default=False)

    #开始加油
    start_refueling = fields.Boolean(default=False)

    #加油结束
    refueling_ended = fields.Boolean(default=False)

    #修车开始
    start_maintenance = fields.Boolean(default=False)

    #修车结束
    maintenance_ended = fields.Boolean(default=False)

    #空放开始
    start_release = fields.Boolean(default=False)

    #空放结束
    release_ended = fields.Boolean(default=False)

    #弹出手动命令窗口
    open_command_window = fields.Boolean(default=False)

    #显示已处理时间
    show_processed = fields.Boolean(default=False)

    #命令窗口显示时长
    command_window_time = fields.Integer()

class Dispatch_setting(models.TransientModel):
    _name = 'dispatch.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)

    # 显示发车异常
    is_show_departure_exception = fields.Boolean(related='company_id.is_show_departure_exception')

    # 显示车辆置顶
    is_show_vehicle_top = fields.Boolean(related='company_id.is_show_vehicle_top')

    # 显示车辆掉线
    is_show_vehicle_dropped = fields.Boolean(related='company_id.is_show_vehicle_dropped')

    # 显示设备异常
    is_display_device_exception = fields.Boolean(related='company_id.is_display_device_exception')

    # 显示车辆超速
    is_show_vehicle_speeding = fields.Boolean(related='company_id.is_show_vehicle_speeding')

    # 显示车辆离线离开
    is_show_vehicle_offline = fields.Boolean(related='company_id.is_show_vehicle_offline')

    # 显示开关车门
    is_display_switch_door = fields.Boolean(related='company_id.is_display_switch_door')

    # 显示乘客纠纷
    is_show_passenger_disputes = fields.Boolean(related='company_id.is_show_passenger_disputes')

    # 显示计划误点
    is_show_plans_are_delayed = fields.Boolean(related='company_id.is_show_plans_are_delayed')

    # 显示疑似抛锚
    is_show_suspected_down = fields.Boolean(related='company_id.is_show_suspected_down')

    # 显示超速
    is_show_overspeed = fields.Boolean(related='company_id.is_show_overspeed')

    # 只显示多少时速以上的提示
    speed_limit = fields.Integer(related='company_id.speed_limit')

    # 超速时自动弹出视频
    is_speeding_automatically_video = fields.Boolean(related='company_id.is_speeding_automatically_video')

    # 报警时自动弹出视频
    is_alarm_automatically_video = fields.Boolean(related='company_id.is_alarm_automatically_video')

    # 疑似抛锚时自动弹出视频
    is_anchor_automatically_video = fields.Boolean(related='company_id.is_anchor_automatically_video')

    # 同意请求派班
    is_agree_ask = fields.Boolean(related='company_id.is_agree_ask')

    # 签到立即派班
    is_attendance_ask = fields.Boolean(related='company_id.is_attendance_ask')

    # 不签到不派班
    is_unattendance_ask = fields.Boolean(related='company_id.is_unattendance_ask')

    # 是否允许
    is_send_plan_to_vehicle = fields.Boolean(related='company_id.is_send_plan_to_vehicle')

    # 提前发送时间
    send_plan_advance_time = fields.Integer(related='company_id.send_plan_advance_time')

    # 车到站点为开车门
    open_the_door = fields.Boolean(related='company_id.open_the_door')

    # 车行走中未关车门
    not_closed_the_door = fields.Boolean(related='company_id.not_closed_the_door')

    # 车未关车门离站
    out_not_closed_the_door = fields.Boolean(related='company_id.out_not_closed_the_door')

    # 非站点开车门
    non_site_driving_door = fields.Boolean(related='company_id.non_site_driving_door')

    # 取消发车计划
    cancel_departure_plan = fields.Boolean(related='company_id.cancel_departure_plan')

    # 司机命令
    driver_command = fields.Boolean(related='company_id.driver_command')

    # 司机上班签到时
    driver_goes_to_work = fields.Boolean(related='company_id.driver_goes_to_work')

    # 司机下班签退时
    driver_checked_out = fields.Boolean(related='company_id.driver_checked_out')

    # 安排司机短休时
    driver_short_break = fields.Boolean(related='company_id.driver_short_break')

    # 进出考核大站时
    big_station = fields.Boolean(related='company_id.big_station')

    # 发车计划误点时
    plan_to_be_delayed = fields.Boolean(related='company_id.plan_to_be_delayed')

    # 车辆超载时
    vehicle_overload = fields.Boolean(related='company_id.vehicle_overload')

    # 开始加油
    start_refueling = fields.Boolean(related='company_id.start_refueling')

    # 加油结束
    refueling_ended = fields.Boolean(related='company_id.refueling_ended')

    # 修车开始
    start_maintenance = fields.Boolean(related='company_id.start_maintenance')

    # 修车结束
    maintenance_ended = fields.Boolean(related='company_id.maintenance_ended')

    # 空放开始
    start_release = fields.Boolean(related='company_id.start_release')

    # 空放结束
    release_ended = fields.Boolean(related='company_id.release_ended')

    # 弹出手动命令窗口
    open_command_window = fields.Boolean(related='company_id.open_command_window')

    # 显示已处理时间
    show_processed = fields.Boolean(related='company_id.show_processed')

    # 命令窗口显示时长
    command_window_time = fields.Integer(related='company_id.command_window_time')

    @api.multi
    def execute(self):
        res = super(Dispatch_setting, self).execute()
        res = self.env['ir.actions.act_window'].for_xml_id('lty_dispatch_config', 'action_dispatch_config_settings')
        return res