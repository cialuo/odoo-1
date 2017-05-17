# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class MaintainRepairCalculate(models.Model):
    """
    车辆维修管理：结算单
    """

    _inherit = 'maintain.manage.repair'

    calculate_result = fields.Selection([('calculating', 'calculating'),
                                       ('calculated', 'calculated')], string="Calculate Result", default='calculating')
    # 结算时间
    calculate_time = fields.Datetime("Calculate Time")

    total_work_time = fields.Float()
    total_work_fee = fields.Float()
    total_product_fee = fields.Float()
    total_fee = fields.Float()
