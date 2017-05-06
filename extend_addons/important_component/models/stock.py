# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class StockMove(models.Model):
    _inherit = 'stock.move'

    component_ids = fields.Many2many('product.component', 'component_move_rec', id1='move_id', id2='component_id',
                                     domain="[('product_id', '=', product_id), ('state', '=', 'avaliable')])")
    @api.multi
    @api.constrains('product_uom_qty', 'component_ids')
    def _check_component_qty(self):
        for move in self:
            if len(move.component_ids) > move.product_uom_qty:
                raise UserError(_('Component qty can not greate than product qty!'))
    @api.multi
    def action_done(self):
        """
        库存移动完成时，如果类型是收货，则进行重要部件过滤及自动编号
        :return:
        """
        res = super(StockMove, self).action_done()
        com_obj = self.env['product.component']
        receipts = self.env['stock.picking.type'].with_context({'lang': 'en'}).sudo().search([('name', 'ilike', 'Receipts')])
        for move in self:
            #库存移动是收货
            if move.picking_type_id in receipts:
                #物资是特别管理，且是重要部件管理
                if move.product_id.is_important and move.product_id.important_type == 'component':
                    for x in range(int(move.product_uom_qty)):
                        com_obj.create({
                            'product_id': move.product_id.id,
                            'location_id': move.location_dest_id.id,
                            'move_id': move.id,
                            'state': 'avaliable',
                        })
            if move.component_ids:
                """
                如果库存移动中，有重要部件清单
                1：调拨单目标库位为车辆库位，重要部件更新为 正在服役，位置为：车辆实库
                2：调拨单目标库位为旧货库位，重要部件更新为 在库待修，位置为：旧货库位
                """
                vals = {}
                vals['location_id'] = move.picking_id.location_dest_id.id
                if move.picking_id and move.picking_id.location_dest_id.is_vehicle:
                    vals['state'] = 'inuse'
                location_old = self.env.ref('stock_picking_types.stock_location_old_to_new').id
                if move.picking_id and move.picking_id.location_dest_id == location_old:
                    vals['state'] = 'waiting_repare'
                move.component_ids.write(vals)
        return res

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_confirm(self):
        """
        加入重要部件管理
        :return: 
        """
        for order in self:
            type = order.picking_type_id.name
            if type in [u'发料', u'领料', u'退料']:
                if all([p.is_important == False for p in order.move_lines.mapped('product_id')]):
                    return super(StockPicking, self).action_confirm()
                elif all([p.is_important == True for p in order.move_lines.mapped('product_id')]):
                    obj = order.repair_id or order.warranty_order_id
                    location_id = obj.vehicle_id.location_stock_id.id  # 车的实库
                    location_dest_id = self.env.ref('stock_picking_types.stock_location_old_to_new').id
                    if type == u'退料':
                        order.write({'location_id': obj.vehicle_id.location_stock_id.id})
                    elif type == u'领料':
                        try:
                            if obj > self.env['maintain.manage.repair']:
                                self.check_product_avail_repair(type, order)
                                self._gen_old_new_picking_repair(order, order.move_lines, location_id, location_dest_id)
                        except TypeError:
                            self.check_product_avail_warranty(type, order)
                            self._gen_old_new_picking_warranty(order, order.move_lines, location_id, location_dest_id)
                    else:
                        try:
                            if obj > self.env['maintain.manage.repair']:
                                # order.move_lines.write({'component_ids': [(6,0,order.repair_id.component_ids.ids)]})
                                o2n_picking = self._gen_old_new_picking_repair(order, order.move_lines, location_id, location_dest_id)
                                if o2n_picking:
                                    o2n_picking.move_lines.write({'component_ids': [(6, 0, order.repair_id.component_ids.ids)]})

                        except TypeError:
                            o2n_picking = self._gen_old_new_picking_warranty(order, order.move_lines, location_id, location_dest_id)
                            if o2n_picking:
                                o2n_picking.move_lines.write({'component_ids': [(6, 0, order.warranty_order_id.component_ids.ids)]})
                else:
                    no_import_products = order.move_lines.mapped('product_id').filtered(lambda x: not x.is_important)
                    remove_products = ','.join([i.name for i in no_import_products])
                    raise UserError(_('There are important & not important components,please remove: %s ') % remove_products)
        return super(StockPicking, self).action_confirm()
