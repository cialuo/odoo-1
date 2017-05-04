# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vehicle_everyday_check(models.Model):
    _name = 'security.vehicle_everyday_check'

    # 车辆编号
    name = fields.Char(string="vehicle_check_number")
    # 车牌号
    plate = fields.Char(string="vehicle_check_plate")
    # 线路
    route = fields.Char(string="vehicle_check_route")
    # 检验日期
    checkout_date = fields.Date(string="vehicle_check_checkout_date")
    # 检查人员
    inspector = fields.Char(string="vehicle_check_inspector")
    # 车辆管理员
    vehicle_manager = fields.Char(string="vehicle_check_manager")
    # 检查结果
    check_result = fields.Char(string="vehicle_check_result")
    # 备注
    remark = fields.Char(string="vehicle_check_remark")
    # 检验类型
    check_type = fields.Char(string="vehicle_check_type")
    # 关联检查表

    check_form = fields.Many2one('security_manage.security_check_table', string="vehicle_check_form", required=True)
    # 计划详情
    # plan_details = fields.One2many("security_manage.security_check_table", "vehicle_check_id")
    # 工作流
    state = fields.Selection([("draft", "vehicle_check_draft"),  # 草稿
                              ("done", "vehicle_check_done"),  # 已检查
                              ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_done(self):
        self.state = 'done'
