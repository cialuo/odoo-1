# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dispatch_abnormal_mgt(models.Model):
    _name = 'dispatch.abnormal.mgt'

    name = fields.Char()
    line_id = fields.Char()
    display = fields.Boolean()
    abnormal_description = fields.Text()
    suggest = fields.Text()
    solution = fields.Text()
    
