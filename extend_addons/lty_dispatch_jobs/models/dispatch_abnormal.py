# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lty_dispatch_abnorma_categ(models.Model):
    _name = 'lty.dispatch.abnorma.categ'

    name = fields.Char(required='1')
    code = fields.Char(required='1')   


class dispatch_abnormal_mgt(models.Model):
    _name = 'dispatch.abnormal.mgt'

    name = fields.Char()
    line_id = fields.Char()
    display = fields.Boolean()
    abnormal_description = fields.Text()
    suggest = fields.Text()
    solution = fields.Text()
    categ_id = fields.Many2one('lty.dispatch.abnorma.categ')
    log_ids = fields.One2many('dispatch.abnormal.logs', 'abnormal_id',  string="logs")
    
    
class dispatch_abnormal_logs(models.Model):
    _name = 'dispatch.abnormal.logs'

    name = fields.Char()
    abnormal_id = fields.Many2one('dispatch.abnormal.mgt')
    user = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    date = fields.Datetime()
    solution = fields.Text()
class dispatch_driving_records(models.Model):
    _name = 'dispatch.driving.records'
    
    name = fields.Char()
    line_id = fields.Char()
    trip_id = fields.Char()
    trip_direction = fields.Char()
    bus_id = fields.Char()
    driver_id = fields.Char()
    plan_mileage = fields.Char()
    gps_mileage = fields.Char()
    plan_start = fields.Datetime()
    actual_start = fields.Datetime()
    plan_end = fields.Datetime()
    actual_end = fields.Datetime()
