# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import timedelta

class MaintainRepare(models.Model):
    _inherit = 'maintain.manage.repair'

    is_important_product = fields.Boolean("Is Important Product")
    important_product_id = fields.Many2one('product.product', related='fault_method_id.important_product_id',
                                           string="Important Product")
    component_ids = fields.Many2many('product.component', 'fleet_manage_maintain_repair_component_rel',
                                     'repair_component_id', 'component_id', 'Component',
                                     copy=False,
                                     domain="[('product_id', '=', important_product_id),('parent_vehicle','=',vehicle_id)]",
                                     states={
                                         'done': [('readonly', True)],
                                         'inspect': [('readonly', True)],
                                         'repair': [('readonly', True)],
                                     })

    @api.onchange('fault_method_id')
    def onchange_method_id(self):
        """
        根据维修办法中关联的重要部件，改变维修单中的信息
        :return: 
        """
        if self.fault_method_id:
            self.fault_reason_id = self.fault_method_id.reason_id
            self.is_important_product = self.fault_method_id.is_important_product
            if self.fault_method_id.is_important_product:
                self.component_ids = self.vehicle_id.mapped('component_ids').filtered(
                    lambda x: x.product_id in self.important_product_id).ids
            self.materials_control = self.fault_method_id.materials_control
        return super(MaintainRepare, self).onchange_method_id()

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
            super(MaintainRepare, self)._generate_picking(im_products, im_location)
            super(MaintainRepare, self)._generate_picking(products - im_products, location)
        else:
            super(MaintainRepare, self)._generate_picking(products, location)


class RepareMethod(models.Model):
    _inherit = 'maintain.fault.method'

    is_important_product = fields.Boolean("Is Important Product")
    important_product_id = fields.Many2one('product.product', string="Important Product",
                                           domain=[('is_important', '=', True)])