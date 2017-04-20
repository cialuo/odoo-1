# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class FleetVehicle(models.Model):
    """
     车辆
    """
    _inherit = 'fleet.vehicle'

    # repair_count = fields.Integer(compute="_compute_repair_count", string='Repairs')

    warranty_count = fields.Integer(compute="_compute_warranty_count", string='Warrantys')

    def _compute_warranty_count(self):
        for record in self:
            record.warranty_count = self.env['fleet_warranty_sheet_item'].search_count([('vehicle_id', '=', self.id)])

    @api.multi
    def return_warranty_action_to_open(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('fleet_manage_warranty_maintain', xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id),
                domain=[('vehicle_id', '=', self.id)]
            )
            return res
        return False