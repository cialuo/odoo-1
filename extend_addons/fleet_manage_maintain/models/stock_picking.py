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
        for order in self:
            if order.picking_type_id.name in [u'发料', u'领料']:
                move_lines = []
                products = []
                picking = []
                picking_type = self.env.ref('stock_picking_types.picking_old_to_new_material')  #交旧领新分拣类型
                if order.move_lines and order.move_lines[0].product_id.is_important:
                    location_id = self.repair_id.vehicle_id.location_stock_id.id                         # 车的实库
                    location_dest_id = self.env.ref('stock_picking_types.stock_location_old_to_new').id  # 旧料库
                    products = order.move_lines

                elif order.move_lines and not order.move_lines[0].product_id.is_important:
                    products = order.move_lines.filtered(lambda x: x.product_id.require_trans == True)
                    location_id = self.repair_id.vehicle_id.location_id.id                              #车的虚拟库位
                    location_dest_id = self.env.ref('stock_picking_types.stock_location_old_to_new').id  # 旧料库

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
                        'origin':self.repair_id.name,
                        'location_id': location_id,
                        'location_dest_id': location_dest_id,
                        'picking_type_id': picking_type.id,
                        'repair_id': self.repair_id.id,
                        'move_lines': move_lines
                    })
                if picking:
                    picking.action_assign()
        return res
