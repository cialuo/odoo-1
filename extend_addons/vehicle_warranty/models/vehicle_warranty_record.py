# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class FleetVehicle(models.Model):
    """
     车辆
    """
    _inherit = 'fleet.vehicle'


    warranty_order_project_ids = fields.One2many("warranty_order_project", 'vehicle_id', domain=[('state', '=', 'complete')])

    warranty_order_project_count = fields.Integer(compute="_compute_warranty_order_project_count", string='Warrantys')

    def _compute_warranty_order_project_count(self):
        for record in self:
            record.warranty_order_project_count = self.env['warranty_order_project'].search_count([('vehicle_id', '=', record.id),('state', '=', 'complete')])

    @api.multi
    def action_to_open_warranty(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('vehicle_warranty', xml_id)
            res.update(
                context=dict(self.env.context, default_vehicle_id=self.id),
                domain=[('vehicle_id', '=', self.id), ('state', '=', 'complete')]
            )
            return res
        return False
