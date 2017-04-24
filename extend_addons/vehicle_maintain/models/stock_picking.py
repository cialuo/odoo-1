# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError


class Picking(models.Model):
    _inherit = "stock.picking"

    repair_id = fields.Many2one('fleet_manage_maintain.repair',
                                ondelete='cascade', string="Repair")

    @api.multi
    def action_confirm(self):
        for order in self:
            type = order.picking_type_id.name
            if type in [u'退料'] and self.repair_id:
                location_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位
                self.write({
                    'location_id': location_id
                })

            elif type in [u'发料', u'领料'] and self.repair_id:
                move_lines = []
                products = []
                picking = []
                picking_type = self.env.ref('stock_picking_types.picking_old_to_new_material')  #交旧领新分拣类型
                if order.move_lines:
                    products = order.move_lines.filtered(lambda x: x.product_id.require_trans == True)
                    location_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位
                    location_dest_id = self.env.ref('stock_picking_types.stock_location_old_to_new').id  # 存货/旧料

                for i in products:
                    vals = {
                        'name': 'stock_move_repair',
                        'product_id': i.product_id.id,
                        'product_uom': i.product_uom.id,
                        'product_uom_qty': i.product_uom_qty,
                    }
                    move_lines.append((0, 0, vals))
                if move_lines:
                    picking = self.env['stock.picking'].create({
                        'origin': self.repair_id.name,
                        'location_id': location_id,
                        'location_dest_id': location_dest_id,
                        'picking_type_id': picking_type.id,
                        'repair_id': self.repair_id.id,
                        'move_lines': move_lines
                    })
                if picking:
                    picking.action_confirm()

        return super(Picking, self).action_confirm()