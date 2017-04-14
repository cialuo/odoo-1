# -*- coding: utf-8 -*-

from odoo import models, fields, api

class fleet_important_component(models.Model):
     _name = 'fleet.important_classification'

     name = fields.Char(u'classification_name',required=True)
     classification_no = fields.Char(u'classification_no',required=True)
     classification_describe = fields.Text('classification_describe')
     remarks = fields.Text(u'remarks')

#继承新增
class fleet_product(models.Model):

     _inherit = "product.product"

     #要件类型
     classification_id = fields.Many2one('fleet.important_classification',u'classification_id')

     #部件类型
     component_type = fields.Selection([('is_spare_parts', 'Spare Parts'), ('is_assembly', 'Assembly')],string='Component Type',default='is_spare_parts')

     #零件列表
     father_product_id = fields.Many2one('product.product')
     product_ids = fields.One2many('product.product', 'father_product_id')

     #parent_id = fields.Many2one('product.product', string='Parent Product',related='parent_id.name')

class fleet_component(models.Model):

     _inherit = 'product.component'

     product_img = fields.Binary('product img', related='product_id.image_medium', store=False, readonly=True)

     product_name = fields.Char('product name', related='product_id.name', store=False, readonly=True)

     product_component_type = fields.Selection('product component type',related='product_id.component_type', store=False, readonly=True)

     product_inter_code = fields.Char('product inter code',related='product_id.inter_code', store=False, readonly=True)
