# -*- coding: utf-8 -*-

from odoo import models, fields, api


class lty_dispatch_abnorma_categ(models.Model):
    _name = 'lty.dispatch.abnorma.categ'

    name = fields.Char(required='1')
    code = fields.Char(required='1')   
