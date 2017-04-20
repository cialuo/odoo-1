# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class ImportProductRepairRecord(models.Model):
    """
     重要部件维修记录
    """
    _inherit = 'product.component'

    # repair_count = fields.Integer(compute="_compute_repair_count", string='Repairs')

    warranty_count = fields.Integer(compute="_compute_warranty_count", string='Warrantys')

    # repair_ids = fields.Many2many('fleet_manage_maintain.repair', 'fleet_manage_maintain_repair_component_rel',
    #                                  'component_id', 'repair_component_id', 'Repairs',
    #                               domain=[('state', '=', 'done')])

    warranty_ids = fields.Many2many('fleet_warranty_sheet_item', 'fleet_warranty_sheet_item_component_rel',
                                     'component_id', 'item_component_id', 'Warrantys',
                                  domain=[('state', '=', 'complete')])

    @api.multi
    @api.depends("warranty_ids.component_ids")
    def _compute_warranty_count(self):
        for i in self:
            i.warranty_count = len(i.warranty_ids)

    @api.multi
    def return_warranty_action_to_open(self):
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('fleet_manage_warranty_maintain', xml_id)
            res.update(
                context=dict(self.env.context),
                domain=[('id', 'in', self.warranty_ids.ids),('state', 'in', ['complete'])]
            )
            return res
        return False