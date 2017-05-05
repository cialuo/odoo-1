# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Item(models.Model): # 保修项目
    _name = 'fleet_manage_warranty.item'

    name = fields.Char() # 项目名称
    code = fields.Char() # 项目编码

    state = fields.Selection([ # 状态
        ('in_use', "in_use"), # 在用
        ('filing', "filing"),  # 归档
    ], default='in_use')

    @api.multi
    def action_in_use(self):
        self.state = 'in_use'

    @api.multi
    def action_filing(self):
        self.state = 'filing'

    mode = fields.Many2one('fleet_manage_warranty.mode', 'Mode', ondelete="set null") # 保修方式

    manhour = fields.Float(digits=(6, 1)) # 工时定额

    remark = fields.Char()  # 备注

    is_important_product = fields.Boolean() # 是否重要部件

    important_product_id = fields.Many2one('product.product', string="Important Product", domain=[('is_important', '=', True)]) # 重要部件

    # bom_line_ids = fields.One2many('fleet_manage_warranty.item.line', 'item_id', 'ItemId') # 用料清单

    avail_ids = fields.One2many('fleet_manage_warranty.available_product', 'item_id', string="Products")

    operational_manual = fields.Text() # 作业手册

    inspection_criteria = fields.Text() # 检验标准


class AvailableProduct(models.Model):
    _name = 'fleet_manage_warranty.available_product'

    # method_id = fields.Many2one('fleet_manage_fault.method',
    #     ondelete='cascade', string="Fault Method Name")

    item_id = fields.Many2one('fleet_manage_warranty.item', ondelete='cascade', string="Item Id")  # 保养项目

    product_id = fields.Many2one('product.product', string="Product")
    product_code = fields.Char("Product Code", related='product_id.default_code', readonly=True)
    categ_id = fields.Many2one('product.category', related='product_id.categ_id', string='Product Category', readonly=True)
    uom_id = fields.Many2one('product.uom', 'Unit of Measure', related='product_id.uom_id', readonly=True)
    onhand_qty = fields.Float('Quantity On Hand', related='product_id.qty_available', readonly=True)
    virtual_available = fields.Float('Forecast Quantity', related='product_id.virtual_available', readonly=True)

    require_trans = fields.Boolean("Require Trans", related='product_id.require_trans', readonly=True)
    vehicle_model = fields.Many2many(related='product_id.vehicle_model', relation='product_vehicle_model_rec',
                                      string='Suitable Vehicle', readonly=True)

    description = fields.Text("Product Size", related='product_id.description', readonly=True)

    change_count = fields.Integer("Change Count")
    max_count = fields.Integer("Max Count")
    remark = fields.Text("Remark", help="Remark")

    @api.constrains('change_count', 'max_count')
    def _check_change_count(self):
        for r in self:
            if r.change_count > r.max_count:
                raise exceptions.ValidationError(_("max_count must be greater than or equal to change_count"))


# class ItemLine(models.Model): # 用料清单
#     _name = 'fleet_manage_warranty.item.line'
#     _order = "sequence"
#
#     sequence = fields.Integer('Sequence', default=1) # 序列
#
#     item_id = fields.Many2one('fleet_manage_warranty.item', index=True) # 保养项目
#
#     product_id = fields.Many2one('product.product', 'Product', required=True) # 产品
#
#     product_code = fields.Char('Product Code', related='product_id.default_code', store=True, readonly=True) # 物资编码
#
#     def _get_default_product_category_id(self):
#         return self.env['product.category'].search([], limit=1, order='id').id
#
#     product_category_id = fields.Many2one('product.category', 'Product Category',default=_get_default_product_category_id) # 物资类别
#
#     product_type = fields.Char() # 型号规格
#
#     def _get_default_product_uom_id(self):
#         return self.env['product.uom'].search([], limit=1, order='id').id
#
#     product_uom_id = fields.Many2one('product.uom', 'Product Unit of Measure',
#         default=_get_default_product_uom_id, oldname='product_uom', required=True) # 单位
#
#     default_usage = fields.Float(default=1, digits=(6, 1), required=True) # 默认用量
#     collar_cap = fields.Float(default=1, digits=(6, 1), required=True) # 领用上限
#
#     def _get_default_vehicle_type(self):
#         return self.env['fleet.vehicle.model'].search([], limit=1, order='id').id
#
#     vehicle_type = fields.Many2one("fleet.vehicle.model", default=_get_default_vehicle_type, store=True) # 适用车型 related='vehicle_id.model_id',
#
#     post_old_get_new = fields.Boolean() # 交旧领新
#
#     remark = fields.Char() # 备注


class FleetManageWarrantyMode(models.Model): # 保修方式
    _name = 'fleet_manage_warranty.mode'
    # _order = 'sequence asc'

    name = fields.Char(required=True)

    code = fields.Char() # 编码

    _sql_constraints = [('warranty_mode_name_unique', 'unique(name)', 'Mode name already exists')]