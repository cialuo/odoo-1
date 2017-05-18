# -*- coding: utf-8 -*-

# ic卡管理

from odoo import models, fields, api, _

class ICCard(models.Model):
    """
    IC卡
    """
    _name = 'employees.iccards'
    _rec_name = 'cardsn'

    _sql_constraints = [('card sn unique', 'unique (cardsn)', 'Card SN Can not duplication')]

    # 卡号
    cardsn = fields.Char('card SN')
    # 状态
    status = fields.Selection([
        ('inactive','inactive'),    # 未启用
        ('active','active'),        # 启用
        ('loss','loss'),            # 挂失
        ('broken','broken'),        # 损坏
        ('blockup','blockup'),      # 停用
    ], string='status', default='inactive')
    # 员工
    employee_id = fields.Many2one('hr.employee', string='employee')
    # 启用日期
    active_date = fields.Date(string='active date')
    # 停用日期
    inactive_date = fields.Date(string='inactive date')
    # 停用原因
    inactive_reason = fields.Selection([
        ('loss','loss'),            # 挂失
        ('broken','broken'),        # 损坏
        ('inactive','inactive'),    # 停用
    ],string='inactive reason')