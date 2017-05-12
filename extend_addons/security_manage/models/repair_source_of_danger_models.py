# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class source_of_danger(models.Model):
    _name = 'srp.source_of_danger'
    # 危险源名称 string=_('')
    name = fields.Char(string='source of dange name', required=True)
    # 区域
    area = fields.Char(tring='area', required=True)
    # 位置
    place = fields.Char(tring='place', required=True)
    # 危害性
    risk_evaluate = fields.Char(string='harmful')
    # 危害描述
    danger_desc = fields.Text(string='harmful description')
    # 防范措施
    precautions = fields.Text(string='preventive measures')

    # 归档标志
    active = fields.Boolean(default=True)
    # 状态
    state = fields.Selection([('use', "Use"), ('done', "Done")], default='use')

    @api.multi
    def action_use(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.active = False
