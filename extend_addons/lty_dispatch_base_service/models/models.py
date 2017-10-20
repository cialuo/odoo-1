# -*- coding: utf-8 -*-

from odoo import models, fields, api


class lty_dispatch_base_service(models.Model):
    _name = 'lty.dispatch.base.service'


	
    @api.model
    def get_line_bus(self, line_ids = []):
	    return line_ids
