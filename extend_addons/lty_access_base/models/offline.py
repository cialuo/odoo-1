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

    #预测客流
    prediction_passenger_num = fields.Integer()

    #历史客流
    history_passenger_num = fields.Integer()

    #候车满意度
    waiting_satisfaction = fields.Integer()

    #滞站客流（等车人数）
    stagnant_traffic = fields.Integer()



