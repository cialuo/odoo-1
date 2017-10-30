# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError
import datetime

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

    # 领料时间
    receiving_time = fields.Datetime(string="receive time")

    # 待料时长 小时计
    waiting_time = fields.Float(string="waiting time", compute='computeWaitTime')

    # 是否报警
    needwarning = fields.Char(string="need warning", compute="_genDefaultNeedWarning")

    @api.multi
    def _genDefaultNeedWarning(self):
        for item in self:
            item.needwarning = 'no'

    @api.multi
    @api.depends('create_date', 'receiving_time')
    def computeWaitTime(self):
        for item in self:
            if  item.receiving_time:
                createtime = datetime.datetime.strptime(item.create_date,'%Y-%m-%d %H:%M:%S')
                rectime = datetime.datetime.strptime(item.receiving_time,'%Y-%m-%d %H:%M:%S')
                td = rectime-createtime
                item.waiting_time = round(td.total_seconds()/3600.0,2)

    @api.multi
    def do_new_transfer(self):
        res = super(StockPicking, self).do_new_transfer()
        self.receiving_time = datetime.datetime.utcnow()
        return res

    @api.multi
    def action_confirm(self):
        for order in self:
            type = order.picking_type_id.name
            if order.repair_id:
                self.check_product_avail_repair(type, order)  # 判断是否可以领退料单
            if type in [u'退料'] and order.repair_id:
                location_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位
                order.write({
                    'location_id': location_id
                })
            elif type in [u'发料', u'领料'] and order.repair_id:
                if order.move_lines:
                    products = order.move_lines.filtered(lambda x: x.product_id.require_trans == True)
                    location_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位

                    picking_type = self.env['stock.picking.type'].search(
                        [('name', '=', u'交旧领新'), ('warehouse_id.company_id', 'child_of', self.env.user.company_id.id)])

                    location_dest_id = picking_type.default_location_dest_id.id or picking_type.warehouse_id.lot_stock_id.id

                    # location_dest_id = self.env.ref('stock_picking_types.stock_location_old_to_new').id  # 存货/旧料
                    self._gen_old_new_picking_repair(order, products, location_id, location_dest_id)

        return super(StockPicking, self).action_confirm()

    def check_product_avail_repair(self, type, order):
        res_get = self.env['stock.picking'].search([('repair_id', '=', order.repair_id.id),
                                                    ('picking_type_id.name', 'in', [u'发料', u'领料']),])
        res_back = self.env['stock.picking'].search([('repair_id', '=', order.repair_id.id),
                                                     ('picking_type_id.name', 'in', [u'退料']),])

        if order.repair_id.materials_control:
            if type == u'领料':
                '''
                   统计所有领料单和发料，退料单中这些商品的
                   1，查询pinking中领料，发料在标记为代办以上的状态的单，退料为完成的单 。统计出相应的数量
                   2, 先查询明细行中产品对应可用物料的领用上限
                   3，用统计的数量+明细行的数量 判断是否小于领用上限
                '''
                res_get = res_get.filtered(lambda x: x.state not in ['cancel'])
                res_back = res_back.filtered(lambda x: x.state in ['done'])
                for i in order.move_lines:
                    ret = self.env['maintain.manage.available_product'].search([('product_id', '=', i.product_id.id),
                                                                                ('repair_id', '=', order.repair_id.id)])
                    if not ret:
                        raise UserError(_('product is not exist,please remove:%s') % (i.name,))

                    get_ct = 0
                    back_ct = 0
                    for j in res_get:
                        products = j.move_lines.filtered(
                            lambda x: x.product_id == i.product_id and x.state not in ['draft', 'cancel'])
                        get_ct = get_ct + sum(products.mapped('product_uom_qty'))

                    for k in res_back:
                        products = k.move_lines.filtered(lambda x: x.product_id == i.product_id)
                        back_ct = back_ct + sum(products.mapped('product_uom_qty'))

                    count = i.product_uom_qty + get_ct - back_ct - ret[0].max_count
                    if count > 0:
                        raise UserError(_('%s more than max_count %s') % (i.name, count))

        if type == u'退料':
            '''
               统计所有领料单和发料，退料单中这些商品的
               1，查询pinking中领料，发料在标记为完成的单，退料非取消的单 。统计出相应的数量
               2, 先查询明细行中产品，如果退料单中的商品不存在可领物料中，则抛出不存在此商品，不能退货
               3，如果退料的单大于领料的单，则抛出不能退这么多
            '''
            res_get = res_get.filtered(lambda x: x.state in ['done'])
            res_back = res_back.filtered(lambda x: x.state not in ['cancel'])

            for i in order.move_lines:
                if not order.repair_id.is_method_change: #判断是否是更换领维修方法的抢修单
                    if order.repair_id.materials_control:
                        ret = self.env['maintain.manage.available_product'].search([('product_id', '=', i.product_id.id),
                                                                                    ('repair_id', '=', order.repair_id.id)])
                        if not ret:
                            raise UserError(_('product is not exist,please remove:%s') % (i.name,))
                get_ct = 0
                back_ct = 0
                for j in res_get:
                    products = j.move_lines.filtered(
                        lambda x: x.product_id == i.product_id and x.state in ['done'])
                    get_ct = get_ct + sum(products.mapped('product_uom_qty'))

                for k in res_back:
                    if k == order:
                        continue
                    products = k.move_lines.filtered(lambda x: x.product_id == i.product_id and x.state not in ['cancel'])
                    back_ct = back_ct + sum(products.mapped('product_uom_qty'))

                count = i.product_uom_qty + back_ct - get_ct
                if count > 0:
                    raise UserError(_('%s 不能退料，退料超过个数: %s') % (i.name, count))

    def _gen_old_new_picking_repair(self,order, products, location_id, location_dest_id):
        # picking_type = self.env.ref('stock_picking_types.picking_old_to_new_material')  # 交旧领新分拣类型
        picking_type = self.env['stock.picking.type'].search(
            [('name', '=', u'交旧领新'), ('warehouse_id.company_id', 'child_of', self.env.user.company_id.id)])
        move_lines = []
        picking = []
        for i in products:
            vals = {
                'name': 'stock_move_repair',
                'product_id': i.product_id.id,
                'product_uom': i.product_uom.id,
                'product_uom_qty': i.product_uom_qty,
                'picking_type_id': picking_type.id,
            }
            move_lines.append((0, 0, vals))
        if move_lines:
            picking = self.env['stock.picking'].create({
                'origin': order.repair_id.name,
                'location_id': location_id,
                'location_dest_id': location_dest_id,
                'picking_type_id': picking_type.id,
                'repair_id': order.repair_id.id,
                'move_lines': move_lines
            })
        if picking:
            picking.action_confirm()
        return picking
