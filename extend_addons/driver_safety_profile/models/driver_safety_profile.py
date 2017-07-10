# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions

class SafeKilometer(models.Model): # 安全公里
    _name = 'safe_kilometer'

    name = fields.Char(default="")

    serial_number = fields.Char(string="Serial Number", help='Serial Number', required=True, index=True, copy=False, default='/', readonly=True) # 编号

    start_time = fields.Datetime(string="Start Time", help='Start Time', required=True) # 开始时间

    end_time = fields.Datetime(string="End Time", help='End Time', required=True) # 结束时间

    route_id = fields.Many2one('route_manage.route_manage', string="Route", help='Route', required=True) # 线路

    vehicle_id = fields.Many2one('fleet.vehicle',string="Vehicle No", help='Vehicle No', required=True) # 车辆

    job_number = fields.Char(string="Job Number", help='Job Number', related='employee_id.jobnumber', readonly=True) # 工号

    employee_id = fields.Many2one('hr.employee', string="Employee Name", help='Employee Name', required=True) # 名称

    accumulated_safe_kilometer = fields.Float(digits=(6, 1), string="Accumulated Safe Kilometer", help='Accumulated Safe Kilometer', required=True) # 累计安全公里

    @api.model
    def create(self, vals):
        if vals.get('serial_number', '/') == '/':
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('safe_kilometer') or '/'
        return super(SafeKilometer, self).create(vals)

    @api.constrains('start_time','end_time')
    def check_datetime(self):
        for r in self:
            if r.start_time > r.end_time:
                raise exceptions.ValidationError("Start can not be greater than the end time")

    @api.constrains('accumulated_safe_kilometer')
    def check_accumulated_safe_kilometer(self):
        for r in self:
            if r.accumulated_safe_kilometer < 0:
                raise exceptions.ValidationError("Can not be negative")

class Endorsement(models.Model):  # 违章记录
    _name = 'endorsement'

    name = fields.Char(default="")

    serial_number = fields.Char(string="Serial Number", help='Serial Number', required=True, index=True, copy=False, default='/', readonly=True) # 编号

    occurrence_time = fields.Datetime(string="Occurrence Time", help='Occurrence Time', required=True) # 时间

    location = fields.Char(string="Location", help='Location', required=True) # 地点

    route_id = fields.Many2one('route_manage.route_manage', string="Route", help='Route', required=True) # 线路

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True) # 车辆

    job_number = fields.Char(string="Job Number", help='Job Number', related='employee_id.jobnumber', readonly=True) # 工号

    employee_id = fields.Many2one('hr.employee', string="Employee Name", help='Employee Name', required=True) # 名称

    violation_type = fields.Char(string="Violation Type", help='Violation Type', required=True) # 违章类型

    illegal_reason = fields.Char(string="Illegal Reason", help='Illegal Reason', required=True) # 违章原因

    handle_result = fields.Char(string="Handle Result", help='Handle Result', required=True) # 处理结果

    @api.model
    def create(self, vals):
        if vals.get('serial_number', '/') == '/':
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('endorsement') or '/'
        return super(Endorsement, self).create(vals)


class AccidentRecord(models.Model):  # 事故记录
    _name = 'accident_record'

    name = fields.Char(default="")

    serial_number = fields.Char(string="Serial Number", help='Serial Number', required=True, index=True, copy=False, default='/', readonly=True) # 编号

    occurrence_time = fields.Datetime(string="Occurrence Time", help='Occurrence Time', required=True) # 时间

    location = fields.Char(string="Location", help='Location', required=True) # 地点

    route_id = fields.Many2one('route_manage.route_manage', string="Route", help='Route', required=True) # 线路

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True) # 车辆

    job_number = fields.Char(string="Job Number", help='Job Number',related='employee_id.jobnumber', readonly=True) # 工号

    employee_id = fields.Many2one('hr.employee', string="Employee Name", help='Employee Name', required=True) # 名称

    accident_type = fields.Char(string="Accident Type", help='Accident Type', required=True) # 事故类型

    accident_cause = fields.Char(string="Accident Cause", help='Accident Cause', required=True) # 事故原因

    handle_result = fields.Char(string="Handle Result", help='Handle Result', required=True) # 处理结果

    @api.model
    def create(self, vals):
        if vals.get('serial_number', '/') == '/':
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('accident_record') or '/'
        return super(AccidentRecord, self).create(vals)


class OverspeedRecord(models.Model):  # 超速记录
    _name = 'overspeed_record'

    name = fields.Char(default="")

    serial_number = fields.Char(string="Serial Number", help='Serial Number', required=True, index=True, copy=False, default='/', readonly=True) # 编号

    occurrence_time = fields.Datetime(string="Occurrence Time", help='Occurrence Time', required=True) # 时间

    location = fields.Char(string="Location", help='Location', required=True) # 地点

    route_id = fields.Many2one('route_manage.route_manage', string="Route", help='Route', required=True) # 线路

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True) # 车辆

    job_number = fields.Char(string="Job Number", help='Job Number',related='employee_id.jobnumber', readonly=True) # 工号

    employee_id = fields.Many2one('hr.employee', string="Employee Name", help='Employee Name', required=True) # 名称

    speed = fields.Float(digits=(6, 1), string="Speed", help='Speed', required=True)  # 车速

    speed_limit = fields.Float(digits=(6, 1), string="Speed Limit", help='Speed Limit', required=True)  # 限速

    outrageous = fields.Float(digits=(6, 1), string="Outrageous", help='Outrageous', required=True)  # 超出范围

    @api.model
    def create(self, vals):
        if vals.get('serial_number', '/') == '/':
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('overspeed_record') or '/'
        return super(OverspeedRecord, self).create(vals)


class employee(models.Model):
    _inherit = 'hr.employee'

    safe_kilometer_ids = fields.One2many("safe_kilometer", 'employee_id', string='Safe Kilometer')

    endorsement_ids = fields.One2many("endorsement", 'employee_id', string='Endorsement')

    accident_record_ids = fields.One2many("accident_record", 'employee_id', string='Accident Record')

    overspeed_record_ids = fields.One2many("overspeed_record", 'employee_id', string='Overspeed Record')

