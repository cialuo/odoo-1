# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RescueFleet(models.Model):
    _name = 'rescue_fleet'
    _rec_name='vehicle_no'    

    company = fields.Char(required=True)
    vehicle_no = fields.Char(required=True)
    responsible_person = fields.Char(required=True)
    responsible_telephone = fields.Char()
    stop_address = fields.Char(required=True)
    service_route = fields.Char()
    service_date = fields.Datetime()

