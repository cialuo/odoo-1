# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dispatch_driver_command(models.Model):
    _name = 'dispatch.driver.command'

    #优先级
    proiority = fields.Integer()
    #命令名称
    name = fields.Char()
    #命令编号
    event_code = fields.Integer()
    #命令类型
    command_type_id = fields.Many2one('dispatch.driver.command.type')
    
    _sql_constraints = [
        ('event_code_uniq', 'unique (event_code)', u'事件代码不能重复!')
    ]           
class dispatch_driver_command_type(models.Model):
    _name = 'dispatch.driver.command.type'

    #类型名称
    name = fields.Char()
    #类型编码
    code = fields.Char()
    
    _sql_constraints = [
        ('code_uniq', 'unique (code)', u'类型代码不能重复!')
    ]