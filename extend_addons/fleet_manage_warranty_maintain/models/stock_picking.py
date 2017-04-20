# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError


class Picking(models.Model):
    _inherit = "stock.picking"

    # repair_id = fields.Many2one('fleet_manage_maintain.repair',
    #                             ondelete='cascade', string="Repair")

    maintainsheet_id = fields.Many2one('fleet_warranty_maintain_sheet', ondelete='cascade', string="Maintain Sheet Id")

    # @api.multi
    # def action_assign(self):
    #     '''
    #     判断是否为 发料 领料
    #     :return:
    #     '''
    #
    #     res = super(Picking, self).action_assign()
    #
    #     for order in self:
    #         type = order.picking_type_id.name
    #         if type in [u'发料', u'领料'] and self.maintainsheet_id and  self.state in ('draft','confirmed'):
    #             move_lines = []
    #             products = []
    #             picking = []
    #             picking_type = self.env.ref('stock_picking_types.picking_old_to_new_material')  #交旧领新分拣类型
    #
    #             if type == u'领料':
    #                 import_products = order.move_lines.mapped('product_id').filtered(
    #                     lambda x:  x.is_important)
    #                 no_import_products = order.move_lines.mapped('product_id').filtered(
    #                     lambda x: not x.is_important)
    #
    #                 if import_products and no_import_products:
    #                     str = ','.join([i.name for i in no_import_products])
    #                     raise UserError(_('There are important components,please remove:%s') % (str,))
    #
    #             if order.move_lines and order.move_lines[0].product_id.is_important:
    #                 location_id = self.maintainsheet_id.vehicle_id.location_stock_id.id  # 车的实库 location_id = self.repair_id.vehicle_id.location_stock_id.id
    #                 location_dest_id = self.env.ref('stock_picking_types.stock_location_old_to_new').id  # 存货/旧料
    #                 products = order.move_lines
    #
    #             elif order.move_lines and not order.move_lines[0].product_id.is_important:
    #                 products = order.move_lines.filtered(lambda x: x.product_id.require_trans == True)
    #                 # location_id = self.repair_id.vehicle_id.location_id.id                              #车的虚拟库位
    #                 location_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位
    #                 location_dest_id = self.env.ref('stock_picking_types.stock_location_old_to_new').id  # 存货/旧料
    #
    #             for i in products:
    #                 vals = {
    #                     'name': 'stock_move_repair',
    #                     'product_id': i.product_id.id,
    #                     'product_uom': i.product_uom.id,
    #                     'product_uom_qty': i.product_uom_qty,
    #                 }
    #                 move_lines.append((0, 0, vals))
    #             if move_lines:
    #                 picking = self.env['stock.picking'].create({
    #                     'origin': self.maintainsheet_id.name,
    #                     'location_id': location_id,
    #                     'location_dest_id': location_dest_id,
    #                     'picking_type_id': picking_type.id,
    #                     # 'repair_id': self.repair_id.id,
    #                     'maintainsheet_id': self.maintainsheet_id.id,
    #                     'move_lines': move_lines
    #                 })
    #             if picking:
    #                 picking.action_assign()
    #     return res





    @api.multi
    def action_confirm(self):
        for order in self:
            type = order.picking_type_id.name
            if type in [u'退料'] and self.maintainsheet_id:
                import_products = order.move_lines.mapped('product_id').filtered(
                    lambda x:  x.is_important)
                no_import_products = order.move_lines.mapped('product_id').filtered(
                    lambda x: not x.is_important)

                if import_products and no_import_products:
                    str = ','.join([i.name for i in no_import_products])
                    raise UserError(_('There are important components,please remove:%s') % (str,))
                elif import_products and not no_import_products:  # 重要部件
                    location_id = self.maintainsheet_id.vehicle_id.location_stock_id.id  # 车的实库
                elif not import_products and no_import_products:  # 非重要部件
                    location_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位

                self.write({
                    'location_id': location_id
                })

            elif type in [u'发料', u'领料'] and self.maintainsheet_id:
                move_lines = []
                products = []
                picking = []
                picking_type = self.env.ref('stock_picking_types.picking_old_to_new_material')  #交旧领新分拣类型

                if type in [u'领料']:
                    import_products = order.move_lines.mapped('product_id').filtered(
                        lambda x: x.is_important)
                    no_import_products = order.move_lines.mapped('product_id').filtered(
                        lambda x: not x.is_important)

                    if import_products and no_import_products:
                        str = ','.join([i.name for i in no_import_products])
                        raise UserError(_('There are important components,please remove:%s') % (str,))

                if order.move_lines and order.move_lines[0].product_id.is_important:
                    location_id = self.maintainsheet_id.vehicle_id.location_stock_id.id  # 车的实库
                    location_dest_id = self.env.ref('stock_picking_types.stock_location_old_to_new').id  # 存货/旧料
                    products = order.move_lines

                elif order.move_lines and not order.move_lines[0].product_id.is_important:
                    products = order.move_lines.filtered(lambda x: x.product_id.require_trans == True)
                    # location_id = self.repair_id.vehicle_id.location_id.id                              #车的虚拟库位
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
                        'origin': self.maintainsheet_id.name,
                        'location_id': location_id,
                        'location_dest_id': location_dest_id,
                        'picking_type_id': picking_type.id,
                        'maintainsheet_id': self.maintainsheet_id.id,
                        'move_lines': move_lines
                    })
                if picking:
                    picking.action_confirm()

        return super(Picking, self).action_confirm()

    #
    # @api.multi
    # def action_confirm(self):
    #     for order in self:
    #         if order.picking_type_id.name in [u'退料'] and self.maintainsheet_id:
    #             import_products = order.move_lines.mapped('product_id').filtered(
    #                 lambda x:  x.is_important)
    #             no_import_products = order.move_lines.mapped('product_id').filtered(
    #                 lambda x:  not x.is_important)
    #
    #             if import_products and no_import_products:
    #                 str = ','.join([i.name for i in no_import_products])
    #                 raise UserError(_('There are important components,please remove:%s') % (str,))
    #             elif import_products and not no_import_products:  # 重要部件
    #                 location_id = self.maintainsheet_id.vehicle_id.location_stock_id.id  # 车的实库 location_id = self.repair_id.vehicle_id.location_stock_id.id  # 车的实库
    #                 # location_dest_id = self.env.ref('stock.stock_location_stock').id  # 库存
    #             elif not import_products and no_import_products:  # 非重要部件
    #                 location_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位
    #                 # location_dest_id = self.env.ref('stock.stock_location_stock').id  # 库存
    #
    #             self.write({
    #                 'location_id': location_id
    #             })
    #
    #         if order.picking_type_id.name in [u'领料'] and self.maintainsheet_id:
    #             import_products = order.move_lines.mapped('product_id').filtered(
    #                 lambda x: x.is_important)
    #             no_import_products = order.move_lines.mapped('product_id').filtered(
    #                 lambda x: not x.is_important)
    #
    #             if import_products and no_import_products:
    #                 str = ','.join([i.name for i in no_import_products])
    #                 raise UserError(_('There are important components,please remove:%s') % (str,))
    #
    #
    #     return super(Picking, self).action_confirm()