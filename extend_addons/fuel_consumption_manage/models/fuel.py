# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class FleetVehicleModel(models.Model):
    """
    车型管理
    """
    _inherit = 'fleet.vehicle.model'

    def _default_corrent_ids(self):
        corrent_list = []
        for i in range(1, 16):
            corrent_list.append((0, 0, {'year': i, 'correct_value': 1}))
        return corrent_list

    ave_fuel_consumption = fields.Float(string="Ave Fuel Consumption")
    fuel_consumption = fields.Float('Fuel Consumption', help='Fuel Consumption')

    correct_ids = fields.One2many('fuel_consumption_correction', 'model_id', string="Corrections",
                                  default=_default_corrent_ids)


class FuelConsumptionCorrection(models.Model):
    """
    油耗修正系数
    """
    _name = 'fuel_consumption_correction'

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    model_id = fields.Many2one('fleet.vehicle.model', ondelete='cascade', string="Vehicle Model")
    year = fields.Integer('years', readonly=1)
    correct_value = fields.Float('Correct Value', default=1)
    user_id = fields.Many2one('hr.employee', string="User Name", default=_default_employee, readonly=1)
    write_date = fields.Datetime(readonly=1)

