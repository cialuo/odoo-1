# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BusAlgorithm(models.Model):
    _name = 'bus_algorithm'
    """
    车辆轮班算法
    """
    code = fields.Char("Algorithm Code", required=True)
    name = fields.Char("Algorithm Name", required=True)
    cycle = fields.Integer("Algorithm Cycle",  required=True)
    direction = fields.Selection([('0', '0'),
                                 ('positive', 'positive'),
                                 ('negative', 'negative')
                                 ], default='0',  required=True, string="Algorithm Direction")
    algorithm_note = fields.Text()
    remark = fields.Text()


class BusDriverAlgorithm(models.Model):
    _name = 'bus_driver_algorithm'
    """
    司乘轮班算法
    """
    code = fields.Char("Algorithm Code", required=True)
    name = fields.Char("Algorithm Name", required=True)
    cycle = fields.Integer("Algorithm Cycle",  required=True)
    direction = fields.Selection([('0', '0'),
                                 ('positive', 'positive'),
                                 ('negative', 'negative')
                                 ], default='0',  required=True, string="Algorithm Direction")
    algorithm_note = fields.Text()
    remark = fields.Text()