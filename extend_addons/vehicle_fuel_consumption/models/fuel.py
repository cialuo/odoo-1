# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Vehicle(models.Model):
    """
    车辆档案
    """
    _inherit = "fleet.vehicle"

    '''
        车型额定油耗
        年限修正系数
        线路修正系数
        额定油耗油耗
        营运油耗
        超额
    '''
    model_fuel_consumption = fields.Float('Model Fuel Consumption', related='model_id.fuel_consumption', store=True,
                                          readonly=True, copy=False)
    correct_value = fields.Float(compute='_get_correct_value', readonly=True, copy=False)
    route_correct_value = fields.Float(store=True, copy=False)

    fuel_consumption = fields.Float('Model Fuel Consumption', compute='_get_fuel_consumption',
                                    store=True, readonly=True, copy=False)
    real_consumption = fields.Float('Real Consumption', copy=False)

    excess_consumption = fields.Float('Excess Consumption', compute='_get_fuel_consumption',
                                      readonly=True, copy=False)

    @api.depends('service_year', 'model_id')
    def _get_correct_value(self):
        for i in self:
            res = self.env['vehicle.fuel_consumption_correction'].search([('model_id', '=', i.model_id.id),
                                                            ('year', '=', i.service_year)])
            if res:
                i.correct_value= res[0].correct_value


    @api.depends('model_fuel_consumption','correct_value','route_correct_value','real_consumption')
    def _get_fuel_consumption(self):
        for i in self:
            i.fuel_consumption = i.model_fuel_consumption*i.correct_value*i.route_correct_value
            i.excess_consumption = i.real_consumption - i.model_fuel_consumption*i.correct_value*i.route_correct_value



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

    correct_ids = fields.One2many('vehicle.fuel_consumption_correction', 'model_id', string="Corrections",
                                  default=_default_corrent_ids)


class FuelConsumptionCorrection(models.Model):
    """
    油耗修正系数
    """
    _name = 'vehicle.fuel_consumption_correction'

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    model_id = fields.Many2one('fleet.vehicle.model', ondelete='cascade', string="Vehicle Model")
    year = fields.Integer('years', readonly=1)
    correct_value = fields.Float('Correct Value', default=1)
    user_id = fields.Many2one('hr.employee', string="User Name", default=_default_employee, readonly=1)
    write_date = fields.Datetime(readonly=1)

