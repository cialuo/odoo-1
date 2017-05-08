# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vehicle_abarbeitung_check(models.Model):
    _name = 'security.vehicle_abarbeitung_check'

    @api.multi
    def _add_plan_details(self):
        res = self.env['security_manage.check_table'].search([("function_module", "=", u"车辆整改检查")])
        datas = []
        for i in res[0].plan_detail:
            data = {
                "item_id": i.item_id,
                "check_item_name": i.check_item_name,
                "check_content": i.check_content,
                "check_standards": i.check_standards
            }
            datas.append((0, 0, data))
        print datas
        return datas

    # 车辆编号
    name = fields.Many2one('fleet.vehicle', string="vehicle_check_number", required=True)
    # 车牌号
    plate = fields.Char(string="vehicle_check_plate", related='name.license_plate', store=False, readonly=True)
    # 线路
    route = fields.Char(string='vehicle_check_route')
    # route = fields.Many2one('vehicle_manage.route', related='name.route_id', store=False)
    # 检验日期
    checkout_date = fields.Date(string="vehicle_check_checkout_date")
    # 检查人员
    inspector = fields.Many2one("hr.employee", string="vehicle_check_inspector")
    # 车辆管理员
    vehicle_manager = fields.Many2one('res.users', string="vehicle_check_manager",
                                      required=True, default=lambda self: self.env.user)
    # 检查结果
    check_result = fields.Char(string="vehicle_check_result")
    # 备注
    remark = fields.Char(string="vehicle_check_remark")
    # 检验类型
    check_type = fields.Char(string="vehicle_check_type")
    # # 关联检查表
    # check_form = fields.Many2one('security.vehicle_plan_details')
    # 计划详情
    plan_details_id = fields.One2many("security.vehicle_plan_details", "vehicle_abarbeitung_check_id", default=_add_plan_details)
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
