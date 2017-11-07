# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Card(models.Model):
    _name = 'line.card'

    name = fields.Char(string="line name", required=True)
    city = fields.Integer(string="line city", required=True)
    company = fields.Integer(string="line company", required=True)
    type = fields.Integer([(1, 'common')], default='common', string="line type", required=True)
    putonghua = fields.Char(string="line putonghua")
    english = fields.Char(string="line english")
    dialect = fields.Char(string="line dialect")

    up_speed = fields.Integer(string="line up speed")
    down_speed = fields.Integer(string="line down speed")




