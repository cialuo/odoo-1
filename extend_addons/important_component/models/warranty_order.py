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
            super(WarrantyOrder, self)._generate_picking(im_products, im_location)
            super(WarrantyOrder, self)._generate_picking(products - im_products, location)
        else:
            super(WarrantyOrder, self)._generate_picking(products, location)