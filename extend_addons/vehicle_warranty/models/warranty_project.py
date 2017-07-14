# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class WarrantyProject(models.Model): # 保修项目
    _name = 'warranty_project'

    name = fields.Char(string='Project Name', required=True) # 项目名称
    code = fields.Char(string='Project Code', required=True) # 项目编码

    state = fields.Selection([ # 状态
        ('use', "use"), # 在用
        ('done', "Filing"),  # 归档
    ], default='use', string="MyState")

    active = fields.Boolean(string="MyActive", default=True)

    @api.multi
    def action_in_use(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_filing(self):
        self.state = 'done'
        self.active = False

    mode = fields.Many2one('warranty_mode', 'Mode', ondelete="set null") # 保修方式

    manhour = fields.Float(digits=(6, 1), default=1) # 工时定额

    remark = fields.Char()  # 备注

    # is_important_product = fields.Boolean() # 是否重要部件

    # important_product_id = fields.Many2one('product.product', string="Important Product", domain=[('is_important', '=', True)]) # 重要部件

    avail_ids = fields.One2many('warranty_project_product', 'project_id', string="Products") # 用料清单

    operational_manual = fields.Text() # 作业手册

    inspection_criteria = fields.Text() # 检验标准


class WarrantyProjectProduct(models.Model): # 维保项目_用料清单
    _name = 'warranty_project_product'

    project_id = fields.Many2one('warranty_project', ondelete='cascade', string="Warranty Project")  # 保养项目

    product_id = fields.Many2one('product.product', string="Product")
    product_code = fields.Char("Product Code", related='product_id.default_code', readonly=True)
    categ_id = fields.Many2one('product.category', related='product_id.categ_id', string='Warranty Category', readonly=True)
    uom_id = fields.Many2one('product.uom', 'Unit of Measure', related='product_id.uom_id', readonly=True)
    onhand_qty = fields.Float('Quantity On Hand', related='product_id.qty_available', readonly=True)
    virtual_available = fields.Float('Forecast Quantity', related='product_id.virtual_available', readonly=True)

    list_price = fields.Float(related='product_id.list_price', readonly=True)

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


class WarrantyMode(models.Model): # 维保方式
    _name = 'warranty_mode'
    # _order = 'sequence asc'

    name = fields.Char(required=True)

    code = fields.Char(required=True) # 编码

    _sql_constraints = [('warranty_mode_name_unique', 'unique(name)', 'Mode name already exists')]