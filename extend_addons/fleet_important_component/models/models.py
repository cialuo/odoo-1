# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions,_

class fleet_important_component(models.Model):

     _name = 'fleet.important_classification'

     """
          新增要件分类表
     """

     name = fields.Char('classification_name',required=True)
     classification_no = fields.Char('classification_no',required=True)
     classification_describe = fields.Text('classification_describe')
     remarks = fields.Text('remarks')


class fleet_product_component(models.Model):
     _name = 'product.parts_list'

     """
          新增零件列表：
               物资，数量

               虚拟字段：
                    物资名称，物资规格，物资编码
     """

     #用于重要部件与零件列表之间的关联关系
     product_id = fields.Many2one('product.product')

     #用于零件列表与物资之间的关联关系
     product_parts = fields.Many2one('product.product')

     parts_number = fields.Integer('parts_number', required=True)

     product_code = fields.Char('product code', related='product_parts.default_code', store=False, readonly=True)

     product_specifications = fields.Text('product specifications', related='product_parts.description', store=False, readonly=True)



class fleet_product(models.Model):

     _inherit = "product.product"

     """
          继承重写物资表：
               新增重要部件的要件分类属性
               新增重要部件的要件类型
               新增关系重要部件 - 物资
     """

     #要件类型
     classification_id = fields.Many2one('fleet.important_classification','classification_id')

     #部件类型
     component_type = fields.Selection([('is_spare_parts', 'Spare Parts'), ('is_assembly', 'Assembly')],string='Component Type',default='is_spare_parts')

     #零件列表
     parts_ids = fields.One2many('product.parts_list', 'product_id')

     @api.depends('qty_available')
     def _compute_number_of_libraries(self):
          """
               根据在手数量，计算出在库数量
               在库数量 = 在手数量 - 随车数量
          :return:
          """
          for product in self:
               #取重要部件
               if product.important_type == 'component':
                    domain = ['&',('product_id', '=', product.id),('parent_vehicle','!=',None)]
                    count = self.env['product.component'].search_count(domain)
                    product.number_of_libraries = product.qty_available - count
          return self

     #在库数量
     number_of_libraries = fields.Float('Number of Libraries',compute=_compute_number_of_libraries)

     @api.multi
     def write(self, vals):

          if vals.get('component_type')=='is_spare_parts':
               if len(self.parts_ids) > 0:
                    raise exceptions.UserError(_("There is part data, so it cannot be modified!"))

          result = super(fleet_product, self).write(vals)

          return result


class fleet_component(models.Model):

     _inherit = 'product.component'

     """
             重写要见表，用于显示
     """

     product_img = fields.Binary('product img', related='product_id.image_medium', store=False, readonly=True)

     product_name = fields.Char('product name', related='product_id.name', store=False, readonly=True)

     product_component_type = fields.Selection('product component type',related='product_id.component_type', store=False, readonly=True)

     product_inter_code = fields.Char('product inter code',related='product_id.default_code', store=False, readonly=True)

     odometer_progress =fields.Float(string='odometer progress', compute='_get_odometer_progress')

     @api.depends('odometer','product_id.lifetime')
     def _get_odometer_progress(self):
          for component in self:
               if component.product_id.lifetime > 0:
                    component.odometer_progress = round(100.0 * (component.product_id.lifetime-component.odometer) / component.product_id.lifetime, 2)
               else:
                    component.odometer_progress=0.0

