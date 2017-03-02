# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Fault(models.Model):
    """
    """
    _name = 'fleet_manage_fault.fault'
    name = fields.Char(help='Name')