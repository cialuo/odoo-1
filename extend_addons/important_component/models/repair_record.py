# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class ImportProductRepairRecord(models.Model):
    """
     重要部件维修记录
    """
    _inherit = 'product.component'

    repair_count = fields.Integer(compute="_compute_repair_count", string='Repairs')

    repair_ids = fields.Many2many('maintain.manage.repair', 'fleet_manage_maintain_repair_component_rel',
                                     'component_id', 'repair_component_id', 'Repairs',
                                  domain=[('state', '=', 'completed')])

    @api.multi
    @api.depends("repair_ids.component_ids")
    def _compute_repair_count(self):
        for i in self:
            i.repair_count = len(i.repair_ids)

    @api.multi
    def action_to_open(self):
        """
        报修单:
            功能：跳转到维修单
        """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('vehicle_maintain', xml_id)
            res.update(
                context=dict(self.env.context),
                domain=[('id', 'in', self.repair_ids.ids), ('state', 'in', ['completed'])]
            )
            return res
        return False
class ImportProductRepairRecord(models.Model):
    """
     重要部件保养记录
    """
    _inherit = 'product.component'

    warranty_count = fields.Integer(compute="_compute_warranty_count", string='Warrantys')
    warranty_ids = fields.Many2many('warranty_order_project', 'fleet_warranty_sheet_item_component_rel',
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
            res = self.env['ir.actions.act_window'].for_xml_id('vehicle_warranty', xml_id)
            res.update(
                context=dict(self.env.context),
                domain=[('id', 'in', self.warranty_ids.ids),('state', 'in', ['complete'])]
            )
            return res
        return False