# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError


class station_gps_collect_wizard(models.TransientModel):
    _name = 'station.gps.collect.wizard'

    name = fields.Char()
    station_id = fields.Many2one('opertation_resources_station', 'Station', required=True)

    @api.model
    def default_get(self, fields):
        res = super(station_gps_collect_wizard, self).default_get(fields)
        res['station_id'] = self.env.context.get('active_id')
        return res

    @api.multi
    def done_collect(self):
        return