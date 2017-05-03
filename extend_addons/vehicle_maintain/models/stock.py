# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _quants_get_reservation(self, quantity, move, ops=False, domain=None, **kwargs):
        domain = domain if domain is not None else [('qty', '>', 0.0)]
        if move.picking_type_id.name in [u'发料', u'领料']:
            domain.append(('location_id.is_vehicle', '=', False))
            domain.append(('location_id.scrap_location', '=', False))
        return super(StockQuant, self)._quants_get_reservation(quantity, move, ops, domain, **kwargs)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    repair_id = fields.Many2one('maintain.manage.repair',
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
                if self.repair_id.materials_control:
                    '''
                    统计所有领料单和发料，退料单中这些商品的
                    1,先查询明细行中产品对应可用物料的领用上限
                    2，查询pinking中领料，发料在标记为代办以上的状态的单，退料为完成的单 。统计出相应的数量
                    3，用统计的数量+明细行的数量 判断是否小于领用上限
                    '''
                    if type == u'领料':
                        res_get = self.env['stock.picking'].search([('repair_id', '=', self.repair_id.id),
                                                                ('state', 'not in', ['draft', 'cancel']),
                                                                ('picking_type_id.name', 'in', [u'发料', u'领料']),
                                                                ])
                        res_back = self.env['stock.picking'].search([('repair_id', '=', self.repair_id.id),
                                                                    ('state', 'in', ['done']),
                                                                    ('picking_type_id.name', 'in', [u'退料']),
                                                                    ])
                        for i in order.move_lines:
                            ret = self.env['maintain.manage.available_product'].search([('product_id', '=', i.product_id.id),
                                                                                  ('repair_id', '=', self.repair_id.id)])
                            if not ret:
                                raise UserError(_('product is not exist,please remove:%s') % (i.name,))

                            get_ct = back_ct = count = 0
                            for j in res_get:
                                products = j.move_lines.filtered(lambda x:x.product_id == i.product_id)
                                get_ct= get_ct + sum(products.mapped('product_uom_qty'))

                            for k in res_back:
                                products = k.move_lines.filtered(lambda x:x.product_id == i.product_id)
                                back_ct = back_ct + sum(products.mapped('product_uom_qty'))

                            count = i.product_uom_qty + get_ct - back_ct - ret[0].max_count
                            if count > 0:
                                raise UserError(_('%s more than max_count %s') % (i.name,count))

                move_lines = []
                products = []
                picking = []
                picking_type = self.env.ref('stock_picking_types.picking_old_to_new_material')  #交旧领新分拣类型
                if order.move_lines:
                    products = order.move_lines.filtered(lambda x: x.product_id.require_trans==True)
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

        return super(StockPicking, self).action_confirm()