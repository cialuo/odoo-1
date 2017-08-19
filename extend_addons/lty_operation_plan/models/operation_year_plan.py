# -*- coding: utf-8 -*-

from odoo import models, fields, api



class operation_plan_year_lines(models.Model):
    _name = 'operation.plan.year.lines'
    	
    company_id = fields.Many2one('res.company')
    income_tongbi = fields.Float()
    income_huanbi = fields.Float()
    imcome_plan = fields.Float()
    passenger_tongbi = fields.Integer()
    passenger_huanbi = fields.Integer()
    passenger_paln = fields.Integer()
    distance_tongbi = fields.Float()
    distance_huanbi = fields.Float()
    distance_plan = fields.Float()
    note = fields.Text()
    plan_id = fields.Many2one('operation.plan.year')
	
class operation_plan_year_done(models.Model):
    _name = 'operation.plan.year.done'
    	
    company_id = fields.Many2one('res.company')
    imcome_plan = fields.Float()
    imcome_actual = fields.Float()
    passenger_paln = fields.Integer()
    passenger_actual = fields.Integer()
    distance_plan = fields.Float()
    distance_actual = fields.Float()
    plan_id = fields.Many2one('operation.plan.year')
	
	
class operation_plan_year(models.Model):
    _name = 'operation.plan.year'

    name = fields.Char()
    code = fields.Char()
    user_id = fields.Many2one('res.users')
    date = fields.Date()
    company_id = fields.Many2one('res.company')
    imcome_plan = fields.Float()
    plan_passenger = fields.Integer()
    plan_distance = fields.Float()
    note = fields.Char()
    company_id = fields.Many2one('res.company')
