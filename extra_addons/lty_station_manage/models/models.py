# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class chupeng_test(models.Model):
#     _name = 'chupeng_test.chupeng_test'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class Student(models.Model):
    _name = 'lty.station.stu'

    name = fields.Char()
    age = fields.Integer()
    sex = fields.Char()


