# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class StockMove(models.Model):
    _inherit = 'stock.move'

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
                if all([p.is_important == False for p in order.move_lines]):
                    return super(StockPicking, self).action_confirm()
                elif all([p.is_important == True for p in order.move_lines]):
                    obj = order.repair_id or order.warranty_order_id
                    if type == u'退料':
                        order.write({'location_id': obj.vehicle_id.location_stock_id.id})
                    if type == u'领料':
                        pass
                else:
                    raise UserError(_('There are important & not important components '))