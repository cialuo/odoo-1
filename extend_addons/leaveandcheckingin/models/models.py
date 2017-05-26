# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

# 休假与考勤

class attence(models.Model):
    _name = 'employee.attence'


    employee_id = fields.Many2one('he.employee', string='employee')

    # 打卡日期
    recorddate = fields.Date(string='record date')


class attencededucted(models.Model):
    """
    考勤扣款
    """
    _name = 'employee.attencededucted'

    employee_id = fields.Many2one('he.employee', string='employee')

    # 考勤月份
    month = fields.Date(string='attence month')

    # 缺勤时长 分钟单位
    absence = fields.Integer(string='attence absence')

    # 扣款金额
    deducted = fields.Integer(string='deducted money')