# -*- coding: utf-8 -*-

from odoo import models, fields, api


# 解决方案
class dispatch_solution(models.Model):
    _name = 'dispatch.solution'
    _description = 'Dispatch solution'

    # 解决方案名称
    name = fields.Char('Dispatch solution', required=True)
    soulution_id = fields.Many2one('pre.arranged.planning', ondelete='set null')

    # 方案描述
    description = fields.Char('Solution describe')

    # 处理办法前置条件
    precondition = fields.Char('Precondition')

    # 方案状态
    status = fields.Selection([
        ('available', 'Available'),
        ('unavailable', 'Unavailable')],
        string='solution status',
        default='available')
