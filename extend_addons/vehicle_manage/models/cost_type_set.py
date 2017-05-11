# -*- coding: utf-8 -*-

from odoo import models, fields, api

# 费用类型设置
class cost_type_set(models.Model):

    # 表名
    _name = 'cost_type_set.cost_type_set'

    _rec_name = 'type_name'
    # 类型名称
    type_name = fields.Char('Type name', required=True)
    # 备注
    remark = fields.Text('Remark')
    # 是否必选
    is_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='yes', string='Is_required')

    cost_type_id = fields.Many2one('investment_cost', string='investment period cost id')
    # 状态
    WORKFLOW_STATE_SELECTION = [
        ('inuse', 'In-use'),
        ('archive', 'Archive')
    ]

    state = fields.Selection(WORKFLOW_STATE_SELECTION,
                             default='inuse',
                             string='State',
                             readonly=True)

    @api.multi
    def do_inuse(self):
        self.state = 'inuse'
        return True

    @api.multi
    def do_archive(self):
        self.state = 'archive'
        return True