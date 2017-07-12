# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    pick_user = fields.Many2one('res.users', string='Pick User', default=lambda self: self.env.uid,
                                readonly=True, states={'draft': [('readonly', False)]})


class StockMove(models.Model):

    _inherit = 'stock.move'

    #restrict_lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number',#domain=[('id','in','')],
                                      #help="Technical field used to depict a restriction on the lot/serial number of quants to consider when marking this move as 'done'")

    tracking = fields.Selection(related='product_id.tracking', store=True,readonly=True)

    @api.onchange('restrict_lot_id')
    def _onchange_lot(self):
        """
            在系统启用批次的情况下：
                1、物资的批次发生变化时修改单价
                2、如果当前仓库没有当前批次的信息记录单价为0
        :return:
        """
        if self.restrict_lot_id:
            origins = self.restrict_lot_id.mapped('quant_ids').mapped('history_ids').mapped('origin')
            order_lines = self.env['purchase.order'].search([('name', 'in', origins)]).mapped('order_line')
            line = order_lines.filtered(lambda x: x.product_id == self.product_id)
            if line:
                self.price_unit = line[0].price_unit


    @api.onchange('product_id')
    def _onchange_product(self):
        """
            物资发现变化时，修改库存移动的单价：
                1、如果物资的追踪信息不属于批次时，单价为物资的成本价格
                2、如果物资的追踪信息属于批次,则不发生改变
        :return:
        """
        if  self.tracking and self.tracking != "lot":
            self.price_unit = self.product_id.standard_price



