# -*- coding: utf-8 -*-

from odoo import models, fields, api



class Card(models.Model):
    _name = 'route.card'

    name = fields.Char()