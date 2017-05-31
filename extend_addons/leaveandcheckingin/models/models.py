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

class LeaveType(models.Model):
    """
    请假类型
    """
    _inherit = 'hr.holidays.status'
    _rec_name = 'namestr'

    _sql_constraints = [('leave type unique', 'unique (name)', 'leave type code Can not duplication')]

    # 类型名称
    namestr = fields.Char(string='type name')

class LeaveConfig(models.TransientModel):

    _name = 'leave.config.settings'
    _inherit = 'res.config.settings'

    # 加班转调休过期天数
    expiretime = fields.Integer(string='overtime expire time')


class WorkOvertime(models.Model):

    _name = 'leave.workovertime'

    employee_id = fields.Many2one('hr.employee', string='employee')

    # 开始时间
    start = fields.Datetime(string='start time')

    # 结束时间
    end = fields.Datetime(string='end time')

    # 状态
    state = fields.Selection([
        ('draft', 'draft'),             # 草稿
        ('confirmed', 'confirmed'),     # 已确认
        ('done', 'done')                # 已完成
    ], string="status", default='draft')

    # 加班类型
    type = fields.Selection([
        ('default','default'),          # 默认
        ('money','money'),              # 加班费
        ('offset','offset'),            # 调休
    ], string='overtime type')

    # 制表人
    create_user = fields.Many2one('res.users', string='create user', default=lambda self: self._uid)

    # 审批/会签人员
    countersign_person = fields.Many2one('res.users', string="employees_countersign_person")

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.countersign_person = self._uid
        self.state = 'done'
