import logging
import threading

from odoo import api, models, tools, registry

class FuelConsumptionUpdate(models.TransientModel):
    _name = "fuel_consumption.update"
    _description = "Fuel Consumption Update"

    def _default_corrent_ids(self):
        corrent_list = []
        for i in range(1, 16):
            corrent_list.append((0, 0, {'year': i, 'correct_value': 1}))
        return corrent_list

    @api.multi
    def update_fuel_consumption(self):
        res = self.env['fleet.vehicle.model'].search([])
        for i in res:
            if not i.correct_ids:
                i.correct_ids = self._default_corrent_ids()
            else:
                if i.correct_ids[0].year==0:
                    print 111111111111111111
                    for j in i.correct_ids:
                        j.unlink()
                    i.correct_ids = self._default_corrent_ids()
        return False

