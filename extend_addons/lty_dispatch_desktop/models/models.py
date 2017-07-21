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
                "f": [0, 250],
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

            }
        },
            {
                "ab": {
                    "a": "1",
                    "y": "2",
                    "c": "3",
                    "d": [{'name': "武汉", 'status': '1', 'color': '#ffd275'},
                          {'name': "武汉", 'status': '0', 'color': '#cc2123'},
                          {'name': "武汉", 'status': '1', 'color': '#ffd275'},
                          {'name': "武汉", 'status': '1', 'color': '#4dcfc7'},
                          {'name': "武汉", 'status': '1', 'color': '#4dcfc7'},
                          {'name': "武汉", 'status': '1', 'color': '#ffd275'},
                          {'name': "武汉", 'status': '1', 'color': '#aad275'},
                          {'name': "武汉", 'status': '1', 'color': '#cc2123'}],
                    "d2": [{'name': "武汉1", 'status': '0', 'color': '#ffd275'},
                           {'name': "武汉2", 'status': '0', 'color': '#cc2123'},
                           {'name': "武汉", 'status': '1', 'color': '#ffd275'},
                           {'name': "武汉4", 'status': '1', 'color': '#4dcfc7'},
                           {'name': "武汉5", 'status': '1', 'color': '#4dcfc7'},
                           {'name': "武汉5", 'status': '1', 'color': '#d4cfc7'},
                           {'name': "武汉6", 'status': '1', 'color': '#ffd275'},
                           {'name': "武汉7", 'status': '1', 'color': '#cc2123'}],
                    "e": [10, 5, 36, 10, 10, 20,40,58],
                    "f": [0, 0],
                    "g": ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123", "#4dcfc7", "#f69e92", "#f69e92", "#cc2123"],
                    "h": [12, 130, 260],
                    "j": {
                        "line": 32,
                        "car": 14,
                        "good_car": 10,
                        "SignalStatus": "well",
                        "driver": 2
                    },
                    "k": [12, 200, 300, 450, 600, 860,1000, 1170]
                }
            }

        ]
        return dis_desk
