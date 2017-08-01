# -*- coding: utf-8 -*-

from odoo import models, fields, api


class lty_dispatch_desktop(models.Model):
    _name = 'lty_dispatch_desktop.lty_dispatch_desktop'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

    @api.model
    def dispatch_desktop(self, id):
        dis_desk = [
            {
                "oneline": {

                    "id": "12",
                    'line_show_or_hide': {
                    'left': '100',
                    'top': '100',
                    'zIndex': '0',
                    'show': "block"
                },
                'chart_show_or_hide':{
                    'left': '1280',
                    'top': '100',
                    'zIndex': '0',
                    'show': 'block'
                },
                "line_num":[32, 13, 30],
                # 上行站点名称以及是否显示的状态判断，站点对应颜色（实际传对应拥堵状态的一个值，前端换成对应颜色）
                "siteTop": [{'name': "深大", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大", 'status': '0', 'color': '#cc2123'},
                      {'name': "深大", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大", 'status': '1', 'color': '#4dcfc7'},
                      {'name': "深大", 'status': '1', 'color': '#4dcfc7'},
                      {'name': "深大", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大", 'status': '1', 'color': '#cc2123'}],
                # 下行站点名称，是否显示的状态值0和1，站点对应颜色（实际传对应拥堵状态的一个值，前端换成对应颜色）
                "siteBottom": [{'name': "深大1", 'status': '0', 'color': '#ffd275'},
                      {'name': "深大2", 'status': '0', 'color': '#cc2123'},
                      {'name': "深大3", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大4", 'status': '1', 'color': '#4dcfc7'},
                      {'name': "深大5", 'status': '1', 'color': '#4dcfc7'},
                      {'name': "深大6", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大7", 'status': '1', 'color': '#cc2123'}],
                # 整条线路分段拥堵距离显示(在地图上，哪到哪红色，哪到哪绿色，占多长距离)
                "traffic_distance": [10, 2, 36, 10, 10, 20, 58],
                # 趟次计划预测状态（实际传对应计划时间内，计划时间外所定的一个状态值，前端换成对应颜色）
                "plan_feedback": ["#ffd275", "#cc2123", "#4dcfc7", "#f69e92", "#ff4634", "#4dcfc7", "#cc2123"],
                # 单条线路资源，线路名称，车辆数量，机动车辆，状况良好
                "line_info": {
                    "line": 32,
                    "car_num": 14,
                    "list_num":6,
                    "active_car": 10,
                    "bad_car": 4,
                    "share_car":5,
                    "online": 2,
                    "outline":3,
                    "driver":5,
                    "crew":8
                },
                "up_run_car": [
                    {
                        "car_left": 100,
                        "num_car": 12,
                        "type_car": 86
                    },
                    {
                        "car_left": 800,
                        "num_car": 24,
                        "type_car": 5917
                    },
                    {
                        "car_left": 1100,
                        "num_car": 44,
                        "type_car": 351
                    }
                ],
                "down_run_car": [
                    {
                        "car_left": 400,
                        "num_car": 12,
                        "type_car": 597
                    },
                    {
                        "car_left": 100,
                        "num_car": 14,
                        "type_car": 5917
                    }
                ],
                # 站点在控制台分段显示位置（下面数据为自己模拟换算后的离起点的距离）
                "site_to_startpoint": [12, 200, 300, 450, 600, 860, 1170]
            }
            },
            {
                "oneline": {
                    "id": "13",
                    'line_show_or_hide': {
                        'left': '0',
                        'top': '400',
                        'zIndex': '1',
                        'show': 'block'
                    },
                    'chart_show_or_hide': {
                        'left': '1280',
                        'top': '400',
                        'zIndex': '1',
                        'show': 'block'
                    },
                    "siteTop": [{'name': "武汉", 'status': '1', 'color': '#ffd275'},
                          {'name': "武汉", 'status': '0', 'color': '#cc2123'},
                          {'name': "武汉", 'status': '1', 'color': '#ffd275'},
                          {'name': "武汉", 'status': '1', 'color': '#4dcfc7'},
                          {'name': "武汉", 'status': '1', 'color': '#4dcfc7'},
                          {'name': "武汉", 'status': '1', 'color': '#ffd275'},
                          {'name': "武汉", 'status': '1', 'color': '#aad275'},
                          {'name': "武汉", 'status': '1', 'color': '#cc2123'}],
                    "siteBottom": [{'name': "武汉1", 'status': '0', 'color': '#ffd275'},
                           {'name': "武汉2", 'status': '0', 'color': '#cc2123'},
                           {'name': "武汉", 'status': '1', 'color': '#ffd275'},
                           {'name': "武汉4", 'status': '1', 'color': '#4dcfc7'},
                           {'name': "武汉5", 'status': '1', 'color': '#4dcfc7'},
                           {'name': "武汉5", 'status': '1', 'color': '#d4cfc7'},
                           {'name': "武汉6", 'status': '1', 'color': '#ffd275'},
                           {'name': "武汉7", 'status': '1', 'color': '#cc2123'}],
                    "traffic_distance": [10, 5, 36, 10, 10, 20,40,58],
                    "line_num": [32, 13, 30],
                    "plan_feedback": ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123", "#4dcfc7", "#f69e92", "#f69e92", "#cc2123"],
                    "line_info": {
                        "line": 13,
                        "car_num": 11,
                        "list_num":16,
                        "active_car": 20,
                        "bad_car": 4,
                        "share_car":6,
                        "online": 11,
                        "outline":4,
                        "driver":5,
                        "crew":8
                     },
                    "up_run_car":[
                        {
                            "car_left":100,
                            "num_car":12,
                            "type_car":597
                        },
                        {
                            "car_left": 100,
                            "num_car": 14,
                            "type_car": 5917
                        }
                    ],
                    "down_run_car": [
                        {
                            "car_left": 400,
                            "num_car": 12,
                            "type_car": 597
                        },
                        {
                            "car_left": 100,
                            "num_car": 14,
                            "type_car": 5917
                        }
                    ],
                    "site_to_startpoint": [12, 200, 300, 450, 600, 860,1000, 1170]
                }
            }
        ]

        return dis_desk

