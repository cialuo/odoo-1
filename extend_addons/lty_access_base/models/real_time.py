# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lineTimeTopic(models.Model):

    _name = 'real_time.lineTopic'
    _description = 'real_timeLineTopic'

    '''实时线路信息'''

    name = fields.Char()
