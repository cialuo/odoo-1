#-*- coding: utf8 -*-

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    #峰段标识 高/平/低
    marked_peak = fields.Integer(default=20)
    marked_flat_peak = fields.Integer(default=60)
    marked_low_peak = fields.Integer(default=20)

    #满意度加权 高/平/低
    peak_waiting = fields.Integer(default=20)
    peak_ride = fields.Integer(default=80)

    flat_peak_waiting = fields.Integer(default=20)
    flat_peak_ride = fields.Integer(default=80)

    low_peak_waiting = fields.Integer(default=20)
    low_peak_ride = fields.Integer(default=80)

    #候车满意度 高/平/低
    peak_waiting_start_time_duration1 = fields.Integer()
    peak_waiting_end_time_duration1 = fields.Integer()
    peak_waiting_satisfaction1 = fields.Integer()

    peak_waiting_start_time_duration2 = fields.Integer()
    peak_waiting_end_time_duration2 = fields.Integer()
    peak_waiting_satisfaction2 = fields.Integer()

    peak_waiting_start_time_duration3 = fields.Integer()
    peak_waiting_end_time_duration3 = fields.Char(default=u'以上')
    peak_waiting_satisfaction3 = fields.Integer()

    flat_peak_waiting_start_time_duration1 = fields.Integer()
    flat_peak_waiting_end_time_duration1 = fields.Integer()
    flat_peak_waiting_satisfaction1 = fields.Integer()

    flat_peak_waiting_start_time_duration2 = fields.Integer()
    flat_peak_waiting_end_time_duration2 = fields.Integer()
    flat_peak_waiting_satisfaction2 = fields.Integer()

    flat_peak_waiting_start_time_duration3 = fields.Integer()
    flat_peak_waiting_end_time_duration3 = fields.Char(default=u'以上')
    flat_peak_waiting_satisfaction3 = fields.Integer()

    low_peak_waiting_start_time_duration1 = fields.Integer()
    low_peak_waiting_end_time_duration1 = fields.Integer()
    low_peak_waiting_satisfaction1 = fields.Integer()

    low_peak_waiting_start_time_duration2 = fields.Integer()
    low_peak_waiting_end_time_duration2 = fields.Integer()
    low_peak_waiting_satisfaction2 = fields.Integer()

    low_peak_waiting_start_time_duration3 = fields.Integer()
    low_peak_waiting_end_time_duration3 = fields.Char(default=u'以上')
    low_peak_waiting_satisfaction3 = fields.Integer()

    #乘车舒适度 高/平/低
    peak_ride_start_time_duration1 = fields.Integer()
    peak_ride_end_time_duration1 = fields.Integer()
    peak_ride_comfort1 = fields.Integer()

    peak_ride_start_time_duration2 = fields.Integer()
    peak_ride_end_time_duration2 = fields.Integer()
    peak_ride_comfort2 = fields.Integer()

    peak_ride_start_time_duration3 = fields.Integer()
    peak_ride_end_time_duration3 = fields.Char(default=u'以上')
    peak_ride_comfort3 = fields.Integer()

    flat_peak_ride_start_time_duration1 = fields.Integer()
    flat_peak_ride_end_time_duration1 = fields.Integer()
    flat_peak_ride_comfort1 = fields.Integer()

    flat_peak_ride_start_time_duration2 = fields.Integer()
    flat_peak_ride_end_time_duration2 = fields.Integer()
    flat_peak_ride_comfort2 = fields.Integer()

    flat_peak_ride_start_time_duration3 = fields.Integer()
    flat_peak_ride_end_time_duration3 = fields.Char(default=u'以上')
    flat_peak_ride_comfort3 = fields.Integer()

    low_peak_ride_start_time_duration1 = fields.Integer()
    low_peak_ride_end_time_duration1 = fields.Integer()
    low_peak_ride_comfort1 = fields.Integer()

    low_peak_ride_start_time_duration2 = fields.Integer()
    low_peak_ride_end_time_duration2 = fields.Integer()
    low_peak_ride_comfort2 = fields.Integer()

    low_peak_ride_start_time_duration3 = fields.Integer()
    low_peak_ride_end_time_duration3 = fields.Char(default=u'以上')
    low_peak_ride_comfort3 = fields.Integer()

    #额定满载率 高/平/低
    peak_full_load = fields.Integer()
    flat_peak_load = fields.Integer()
    low_peak_full_load = fields.Integer()

    #行车作业计划设置
    generate_time = fields.Char()
    is_advance = fields.Boolean(default=False)
    begin_advance_date = fields.Datetime()
    end_advance_date = fields.Datetime()
    is_general = fields.Boolean(default=False)
    begin_general_date = fields.Datetime()
    end_general_date = fields.Datetime()

class Operation_setting(models.TransientModel):
    _name = 'operation.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)

    # 峰段标识 高/平/低
    marked_peak = fields.Integer(related='company_id.marked_peak')
    marked_flat_peak = fields.Integer(related='company_id.marked_flat_peak')
    marked_low_peak = fields.Integer(related='company_id.marked_low_peak')

    # 满意度加权 高/平/低
    peak_waiting = fields.Integer(related='company_id.peak_waiting')
    peak_ride = fields.Integer(related='company_id.peak_ride')

    flat_peak_waiting = fields.Integer(related='company_id.flat_peak_waiting')
    flat_peak_ride = fields.Integer(related='company_id.flat_peak_ride')

    low_peak_waiting = fields.Integer(related='company_id.low_peak_waiting')
    low_peak_ride = fields.Integer(related='company_id.low_peak_ride')

    # 候车满意度 高/平/低
    peak_waiting_start_time_duration1 = fields.Integer(related='company_id.peak_waiting_start_time_duration1')
    peak_waiting_end_time_duration1 = fields.Integer(related='company_id.peak_waiting_end_time_duration1')
    peak_waiting_satisfaction1 = fields.Integer(related='company_id.peak_waiting_satisfaction1')

    peak_waiting_start_time_duration2 = fields.Integer(related='company_id.peak_waiting_start_time_duration2')
    peak_waiting_end_time_duration2 = fields.Integer(related='company_id.peak_waiting_end_time_duration2')
    peak_waiting_satisfaction2 = fields.Integer(related='company_id.peak_waiting_satisfaction2')

    peak_waiting_start_time_duration3 = fields.Integer(related='company_id.peak_waiting_start_time_duration3')
    peak_waiting_end_time_duration3 = fields.Char(related='company_id.peak_waiting_end_time_duration3')
    peak_waiting_satisfaction3 = fields.Integer(related='company_id.peak_waiting_satisfaction3')

    flat_peak_waiting_start_time_duration1 = fields.Integer(related='company_id.flat_peak_waiting_start_time_duration1')
    flat_peak_waiting_end_time_duration1 = fields.Integer(related='company_id.flat_peak_waiting_end_time_duration1')
    flat_peak_waiting_satisfaction1 = fields.Integer(related='company_id.flat_peak_waiting_satisfaction1')

    flat_peak_waiting_start_time_duration2 = fields.Integer(related='company_id.flat_peak_waiting_start_time_duration2')
    flat_peak_waiting_end_time_duration2 = fields.Integer(related='company_id.flat_peak_waiting_end_time_duration2')
    flat_peak_waiting_satisfaction2 = fields.Integer(related='company_id.flat_peak_waiting_satisfaction2')

    flat_peak_waiting_start_time_duration3 = fields.Integer(related='company_id.flat_peak_waiting_start_time_duration3')
    flat_peak_waiting_end_time_duration3 = fields.Char(related='company_id.flat_peak_waiting_end_time_duration3')
    flat_peak_waiting_satisfaction3 = fields.Integer(related='company_id.flat_peak_waiting_satisfaction3')

    low_peak_waiting_start_time_duration1 = fields.Integer(related='company_id.low_peak_waiting_start_time_duration1')
    low_peak_waiting_end_time_duration1 = fields.Integer(related='company_id.low_peak_waiting_end_time_duration1')
    low_peak_waiting_satisfaction1 = fields.Integer(related='company_id.low_peak_waiting_satisfaction1')

    low_peak_waiting_start_time_duration2 = fields.Integer(related='company_id.low_peak_waiting_start_time_duration2')
    low_peak_waiting_end_time_duration2 = fields.Integer(related='company_id.low_peak_waiting_end_time_duration2')
    low_peak_waiting_satisfaction2 = fields.Integer(related='company_id.low_peak_waiting_satisfaction2')

    low_peak_waiting_start_time_duration3 = fields.Integer(related='company_id.low_peak_waiting_start_time_duration3')
    low_peak_waiting_end_time_duration3 = fields.Char(related='company_id.low_peak_waiting_end_time_duration3')
    low_peak_waiting_satisfaction3 = fields.Integer(related='company_id.low_peak_waiting_satisfaction3')

    # 乘车舒适度 高/平/低
    peak_ride_start_time_duration1 = fields.Integer(related='company_id.peak_ride_start_time_duration1')
    peak_ride_end_time_duration1 = fields.Integer(related='company_id.peak_ride_end_time_duration1')
    peak_ride_comfort1 = fields.Integer(related='company_id.peak_ride_comfort1')

    peak_ride_start_time_duration2 = fields.Integer(related='company_id.peak_ride_start_time_duration2')
    peak_ride_end_time_duration2 = fields.Integer(related='company_id.peak_ride_end_time_duration2')
    peak_ride_comfort2 = fields.Integer(related='company_id.peak_ride_comfort2')

    peak_ride_start_time_duration3 = fields.Integer(related='company_id.peak_ride_start_time_duration3')
    peak_ride_end_time_duration3 = fields.Char(related='company_id.peak_ride_end_time_duration3')
    peak_ride_comfort3 = fields.Integer(related='company_id.peak_ride_comfort3')

    flat_peak_ride_start_time_duration1 = fields.Integer(related='company_id.flat_peak_ride_start_time_duration1')
    flat_peak_ride_end_time_duration1 = fields.Integer(related='company_id.flat_peak_ride_end_time_duration1')
    flat_peak_ride_comfort1 = fields.Integer(related='company_id.flat_peak_ride_comfort1')

    flat_peak_ride_start_time_duration2 = fields.Integer(related='company_id.flat_peak_ride_start_time_duration2')
    flat_peak_ride_end_time_duration2 = fields.Integer(related='company_id.flat_peak_ride_end_time_duration2')
    flat_peak_ride_comfort2 = fields.Integer(related='company_id.flat_peak_ride_comfort2')

    flat_peak_ride_start_time_duration3 = fields.Integer(related='company_id.flat_peak_ride_start_time_duration3')
    flat_peak_ride_end_time_duration3 = fields.Char(related='company_id.flat_peak_ride_end_time_duration3')
    flat_peak_ride_comfort3 = fields.Integer(related='company_id.flat_peak_ride_comfort3')

    low_peak_ride_start_time_duration1 = fields.Integer(related='company_id.low_peak_ride_start_time_duration1')
    low_peak_ride_end_time_duration1 = fields.Integer(related='company_id.low_peak_ride_end_time_duration1')
    low_peak_ride_comfort1 = fields.Integer(related='company_id.low_peak_ride_comfort1')

    low_peak_ride_start_time_duration2 = fields.Integer(related='company_id.low_peak_ride_start_time_duration2')
    low_peak_ride_end_time_duration2 = fields.Integer(related='company_id.low_peak_ride_end_time_duration2')
    low_peak_ride_comfort2 = fields.Integer(related='company_id.low_peak_ride_comfort2')

    low_peak_ride_start_time_duration3 = fields.Integer(related='company_id.low_peak_ride_start_time_duration3')
    low_peak_ride_end_time_duration3 = fields.Char(related='company_id.low_peak_ride_end_time_duration3')
    low_peak_ride_comfort3 = fields.Integer(related='company_id.low_peak_ride_comfort3')

    # 额定满载率 高/平/低
    peak_full_load = fields.Integer(related='company_id.peak_full_load')
    flat_peak_load = fields.Integer(related='company_id.flat_peak_load')
    low_peak_full_load = fields.Integer(related='company_id.low_peak_full_load')

    # 行车作业计划设置
    generate_time = fields.Char(related='company_id.generate_time')
    is_advance = fields.Boolean(related='company_id.is_advance')
    begin_advance_date = fields.Datetime(related='company_id.begin_advance_date')
    end_advance_date = fields.Datetime(related='company_id.end_advance_date')
    is_general = fields.Boolean(related='company_id.is_general')
    begin_general_date = fields.Datetime(related='company_id.begin_general_date')
    end_general_date = fields.Datetime(related='company_id.end_general_date')

    @api.multi
    def execute(self):
        res = super(Operation_setting, self).execute()
        res = self.env['ir.actions.act_window'].for_xml_id('lty_dispatch_config', 'action_operation_config_settings')
        return res