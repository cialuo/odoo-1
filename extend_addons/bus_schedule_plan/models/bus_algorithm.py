# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BusAlgorithm(models.Model):
    _name = 'bus_algorithm'
    """
    车辆轮班算法
    """
    code = fields.Char(readonly=1)
    name = fields.Char(readonly=1)
    cycle = fields.Char(readonly=1)
    direction = fields.Selection([('0', '0'),
                                 ('positive', 'positive'),
                                 ('negative', 'negative')
                                 ], default='0', readonly=1)
    algorithm_note = fields.Text()
    remark = fields.Text()


class BusDriverAlgorithm(models.Model):
    _name = 'bus_driver_algorithm'
    """
    司乘轮班算法
    """
    code = fields.Char(readonly=1)
    name = fields.Char(readonly=1)
    cycle = fields.Char(readonly=1)
    direction = fields.Selection([('0', '0'),
                                 ('positive', 'positive'),
                                 ('negative', 'negative')
                                 ], default='0', readonly=1)
    algorithm_note = fields.Text()
    remark = fields.Text()
