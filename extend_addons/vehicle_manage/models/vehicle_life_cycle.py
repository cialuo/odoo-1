# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


# 车辆生命周期
class vehicle_life(models.Model):
    # 表名(继承fleet.vehicle)
    _inherit = "fleet.vehicle"

    @api.multi
    def _add_default_value(self):
        print('-------------------')
        res = self.env['cost_type_set.cost_type_set'].search([('state', '=', 'inuse')])
        datas = []
        for i in res:
            print ("=======%s" % i.type_name)
            data = {
                'is_required': i.is_required,
                'cost_type': i.type_name,
            }
            datas.append((0, 0, data))
        return datas

    investment_ids = fields.One2many('investment_cost', 'vehicle_id', string='Investments', default=_add_default_value)

    # 状态
    WORKFLOW_STATE_SELECTION = [
        ('invest_period', 'Invest period'),
        ('operation_period', 'Operation period'),
        ('scrap_period', 'Scrap period')
    ]

    vehicle_life_state = fields.Selection(WORKFLOW_STATE_SELECTION,
                                          default='invest_period',
                                          string='Vehicle life cycle state',
                                          readonly=True)

    @api.multi
    def action_operation(self):
        print('operation_period')
        self.vehicle_life_state = 'operation_period'
        self.start_service_date = datetime.date.today()
        return True

    @api.multi
    def action_scrap(self):
        print('scrap_period')
        self.vehicle_life_state = 'scrap_period'
        return True

# 投入期费用
class investment_period_cost(models.Model):
    _name = 'investment_cost'

    _rec_name = 'cost_name'
    # 费用金额
    cost_amount = fields.Integer('Cost amount')
    # 费用名称
    cost_name = fields.Char('Cost name')
    # 发生时间
    occurrence_time = fields.Datetime('Occurrence time')
    # 费用类型
    cost_type = fields.Char('Cost type')
    # 是否必填
    is_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='yes', string='Is_required')
    # 总金额
    total_amount = fields.Integer('Total amount')

    # 状态
    WORKFLOW_STATE_SELECTION = [
        ('inuse', 'In-use'),
        ('archive', 'Archive')
    ]
    vehicle_id = fields.Many2one('fleet.vehicle', string='Investment id')



