# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lty_dispatch_abnorma_categ(models.Model):
    _name = 'lty.dispatch.abnorma.categ'

    name = fields.Char(required='1')
    code = fields.Char(required='1')   


class dispatch_abnormal_mgt(models.Model):
    _name = 'dispatch.abnormal.mgt'

    name = fields.Char()
    #线路
    line_id = fields.Many2one('route_manage.route_manage')
    #是否显示
    display = fields.Boolean()
    #异常描述
    abnormal_description = fields.Text()
    #建议
    suggest = fields.Text()
    #方案
    solution = fields.Text()
    #异常目录
    categ_id = fields.Many2one('lty.dispatch.abnorma.categ')
    #异常日志
    log_ids = fields.One2many('dispatch.abnormal.logs', 'abnormal_id',  string="logs")
    #异常状态
    abnormal_state = fields.Selection([('active', 'Active'), ('ignore', 'Ignore'), ('done', 'Done')],default='active')
    
    @api.multi
    def action_confirm(self):
        """
        """
        self.write({"abnormal_state": 'done'})    
    @api.multi
    def action_ignore(self):
        """
        """
        self.write({"abnormal_state": 'ignore'})        
    
    
    
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
