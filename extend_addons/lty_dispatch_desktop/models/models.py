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
        dis_desk = [{
            "ab": {
                "a": "1",
                "y": "2",
                "c": "3",
                "d": [{'name': "深大", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大", 'status': '0', 'color': '#cc2123'},
                      {'name': "深大", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大", 'status': '1', 'color': '#4dcfc7'},
                      {'name': "深大", 'status': '1', 'color': '#4dcfc7'},
                      {'name': "深大", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大", 'status': '1', 'color': '#cc2123'}],
                "d2": [{'name': "深大1", 'status': '0', 'color': '#ffd275'},
                      {'name': "深大2", 'status': '0', 'color': '#cc2123'},
                      {'name': "深大3", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大4", 'status': '1', 'color': '#4dcfc7'},
                      {'name': "深大5", 'status': '1', 'color': '#4dcfc7'},
                      {'name': "深大6", 'status': '1', 'color': '#ffd275'},
                      {'name': "深大7", 'status': '1', 'color': '#cc2123'}],
                "e": [10, 2, 36, 10, 10, 20, 58],
                "f": [0, 150],
                "g": ["#ffd275", "#cc2123", "#4dcfc7", "#f69e92", "#ff4634", "#4dcfc7", "#cc2123"],
                "h": [12, 130, 260],
                "j": {
                    "line": 32,
                    "car": 14,
                    "good_car": 10,
                    "SignalStatus": "well",
                    "driver": 2
                },
                "k": [12, 200, 300, 450, 600, 860, 1170]

            },
            "cd": {
                "a": "21",
                "y": "13",
                "c": "41",
                "d": ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
                "e": [3, 4, 11, 12, 21, 32],
                "f": [0, 450],
                "g": ["#fff111", "#11FF66", "#dd0033", "#cc2123", "#aa1212", "#3355ff"],
                "h": [12, 130, 260],
                "j": {
                    "line": 32,
                    "car": 24,
                    "good_car": 20,
                    "SignalStatus": "bad",
                    "driver": 12
                }
            }
        }]
        return dis_desk
