# -*- coding: utf-8 -*-
from odoo import models, fields, api


# 调度预案
class pre_arranged_planning(models.Model):
    _name = 'pre.arranged.planning'
    _description = 'Pre-arranged planning'

    # 预案名称
    name = fields.Char('Pre-arranged planning', required=True)

    # 解决方案
    solutions_ids = fields.One2many('dispatch.solution', 'soulution_id', string='All Solutions')

    # 处理办法数量
    number_of_solutions = fields.Integer('Number of Solutions', compute='_compute_number')

    # 命中方式
    hit_mode_ids = fields.One2many('lty.dispatch.abnorma.categ', 'name', string='Hit mode')

    # 30天平均命中次数
    average_hit_times = fields.Integer('Average hit times')

    # 自动套用
    auto_apply = fields.Boolean('Auto apply', default=False, help='Do you want to apply automatically?')

    @api.depends('solutions_ids')
    def _compute_number(self):
        for record in self:
            record.number_of_solutions = len(record.solutions_ids)

