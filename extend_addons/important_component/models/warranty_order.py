# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class WarrantyOrderProject(models.Model): # 保养单_保养项目
    _inherit = 'warranty_order_project'

    component_ids = fields.Many2many('product.component', 'warranty_order_item_component_rel', 'project_component_id', 'component_id', 'Component',
        readonly=True, domain="[('product_id', '=', important_product_id),('parent_vehicle','=',vehicle_id)]")
    important_product_id = fields.Many2one('product.product', related='project_id.important_product_id',
                                           string="Important Product")