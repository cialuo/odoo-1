# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class WarrantyOrderProject(models.Model): # 保养单_保养项目
    _inherit = 'warranty_order_project'

    component_ids = fields.Many2many('product.component', 'warranty_order_item_component_rel', 'project_component_id', 'component_id', 'Component',
        readonly=True, domain="[('product_id', '=', important_product_id),('parent_vehicle','=',vehicle_id)]")
    important_product_id = fields.Many2one('product.product', related='project_id.important_product_id',
                                           string="Important Product")

class WarrantyOrder(models.Model):
    _inherit = 'warranty_order'

    @api.model
    def _generate_picking(self, products, location):
        """
        加入重要部件的开工
        :param products: 生成Picking单据的产品明细
        :param location: 目标库位
        :return: 
        """
        im_products = products.filtered(lambda x: x.product_id.is_important == True)
        if im_products:
            im_location = self.vehicle_id.location_stock_id.id
            picking_type = self.env.ref('stock_picking_types.picking_type_issuance_of_material')
            for p in im_products:
                #找到对应物资的在库备用重要部件，选取更换数量 加入到库存移动中
                domain = [('state', '=', 'avaliable'), ('product_id', '=', p.product_id.id)]
                component_ids = self.env['product.component'].search(domain, limit=p.change_count).ids
                move_lines = []
                picking = []
                vals = {
                    'name': 'stock_move_warranty',
                    'product_id': p.product_id.id,
                    'product_uom': p.product_id.uom_id.id,
                    'product_uom_qty': p.change_count,
                    'component_ids': [(6,0, component_ids)],
                    'picking_type_id': picking_type.id,
                }
                move_lines.append((0, 0, vals))
                if move_lines:
                    picking = self.env['stock.picking'].create({
                        'origin': self.name,
                        'location_id': self.env.ref('stock.stock_location_stock').id,
                        'location_dest_id': im_location,
                        'picking_type_id': picking_type.id,
                        'warranty_order_id': self.id,
                        'move_lines': move_lines
                    })
            # super(WarrantyOrder, self)._generate_picking(im_products, im_location)
            super(WarrantyOrder, self)._generate_picking(products - im_products, location)
        else:
            super(WarrantyOrder, self)._generate_picking(products, location)