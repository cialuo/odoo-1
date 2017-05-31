# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

# 休假与考勤

class attence(models.Model):
    """
    考勤记录
    """
    _name = 'employee.attencerecords'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='employee')

    # 上班打卡时间
    checkingin= fields.Datetime(string='checkingin time')

    # 下班打卡时间
    checkinginout = fields.Datetime(string='checkingout time')

    # 缺勤时长
    length = fields.Integer(string="time length")

    # 状态
    status = fields.Selection([
        ('late','late'),
        ('early','early'),
        ('late+early','late+early')
    ],string='status')


class attencededucted(models.Model):
    """
    考勤扣款
    """
    _name = 'employee.attencededucted'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='employee')

    # 考勤月份
    month = fields.Date(string='attence month')

    # 缺勤时长 分钟单位
    absence = fields.Integer(string='attence absence')

    # 扣款金额
    deducted = fields.Integer(string='deducted money')


class LeaveConfig(models.TransientModel):
    _name = 'leave.config.settings'
    _inherit = 'res.config.settings'

    # 加班转调休过期天数
    expiretime = fields.Integer(string='overtime expire time')