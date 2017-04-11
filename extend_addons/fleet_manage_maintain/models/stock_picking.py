# -*- coding: utf-8 -*-

from odoo import fields, api, models


class Picking(models.Model):
    _inherit = "stock.picking"

    repair_id = fields.Many2one('fleet_manage_maintain.repair',
                                ondelete='cascade', string="Repair")

    @api.multi
    def action_assign(self):
        '''
        判断是否为 发料 领料
        :return:
        '''
        res = super(Picking, self).action_assign()
        if self.picking_type_id.name in [u'发料', u'领料']:
            move_lines = []
            picking_type = self.env.ref('stock_picking_types.picking_old_to_new_material')
            for i in self.repair_id.available_product_ids:
                if i.change_count > 0 and i.require_trans:
                    vals = {
                        'name': 'stock_move_repair',
                        'product_id': i.product_id.id,
                        'product_uom': i.product_id.uom_id.id,
                        'product_uom_qty': i.change_count,
                    }
                    move_lines.append([0, 0, vals])
            if move_lines:
                picking = self.env['stock.picking'].create({
                    'location_id': picking_type.default_location_src_id.id,
                    'location_dest_id': picking_type.default_location_dest_id.id,
                    'picking_type_id': picking_type.id,  # 交旧领新分拣类型
                    'repair_id': self.repair_id.id,
                    'move_lines': move_lines
                })
                picking.action_assign()
        return res
