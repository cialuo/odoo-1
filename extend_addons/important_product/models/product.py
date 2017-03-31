# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from lxml import etree
from datetime import datetime
from odoo.tools.translate import _

class Product(models.Model):
    _inherit = 'product.product'

    """
     扩展产品模块，定义重要部件
     重要部件会包含：适用车型，交旧领新，退役寿命，里程数
     """
    special_attributes = fields.Selection([('common', 'Common'), ('special', 'Special'), ('general', 'General')],
                                          default='common', string='Special Attribute')
    vehicle_model = fields.Many2many('fleet.vehicle.model', 'product_vehicle_model_rec',
                                     id1='product_product_id', id2='vehicle_model_id', string='Suitable Vehicle')
    require_trans = fields.Boolean(string='Old for new', default=False)
    lifetime = fields.Float(string='Lifetime odomter')
    odometer = fields.Float(string='Odometer')
    is_important = fields.Boolean(string='Important', default=False)
    important_type = fields.Selection([('equipment', 'Equipment'), ('component', 'Component'), ('energy', 'Energy')],
                                      string='Important Type')
    parent_id = fields.Many2one('product.product', string='Parent Product')
    inter_code = fields.Char(string='Inter Code')
    default_code = fields.Char(compute='_compute_default_code')
    keeper_id = fields.Many2one('res.users', string='Keeper')
    shelf = fields.Char(string='Shelf')
    contract_price = fields.Float(string='Contract Price')
    tech_ids= fields.One2many('product.tech.info', 'product_id', string='Tec Info')
    component_ids = fields.One2many('product.component', 'product_id', string='Component Info')
    # equipment_ids = fields.One2many('product.equipment', 'product_id', string='Equipment Info')

    _sql_constraints = [
        ('code_parent_category_uniq',
         'unique (inter_code, parent_id, categ_id)',
         _('inter code must unique per product and category'))
    ]

    @api.depends('inter_code', 'categ_id.code', 'parent_id.default_code')
    def _compute_default_code(self):
        """
        根据父产品的编码，产品自编码，产品类别编码计算当前产品的物资编号
        :return:
        """
        for p in self:
            parent_code = ''
            categ_code = ''
            code = ''
            if p.parent_id and p.parent_id.default_code:
                parent_code = p.parent_id.default_code
            if p.categ_id and p.categ_id.code:
                categ_code = p.categ_id.code
            if p.inter_code:
                code = p.inter_code
            p.default_code = parent_code + categ_code + code

class ProductCategory(models.Model):
    _inherit = 'product.category'

    """
    增加产品分类编码，用于物资编号计算
    """

    code = fields.Char(string='Category Code')

class TechInfo(models.Model):
    _name = 'product.tech.info'

    """
    物资技术参数信息
    """

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    standard = fields.Char(string='Standard')
    product_id = fields.Many2one('product.template')
    compare1 = fields.Char(string='Compare1')
    compare2 = fields.Char(string='Compare2')
    parameter1 = fields.Char(string='parameter1')
    parameter2 = fields.Char(string='parameter2')
    description = fields.Text(string='Description')
    note = fields.Char(string='note')

class Component(models.Model):
    _name = 'product.component'
    _order = 'id desc'

    """
    重要部件清单信息
    """

    product_id = fields.Many2one('product.product', string='Product')
    code = fields.Char(string='Component Code', default='/')
    odometer = fields.Float(string='Odometer')
    location_id =fields.Many2one('stock.location', string='Location')
    state = fields.Selection([('avaliable', 'Avaliable'), ('waiting_repare', 'Waiting Repare'),
                              ('inuse', 'Inuse'), ('repareing', 'Repareing')],
                             default='inuse')
    checkout_date = fields.Date(string='Checkout Date')
    move_ids = fields.One2many('stock.move', 'component_id', string='Move lines')
    parent_vehicle = fields.Many2one('fleet.vehicle', string='Vehicle', ondelete='cascade')

    _sql_constraints = [('code_uniq', 'unique (code)', "Code already exists")]

    @api.model
    def create(self, vals):
        """
        自动生成部件编号
        :param vals:
        :return:
        """
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('product_component')
        res = super(Component, self).create(vals)
        return res

    # @api.onchange('parent_vehicle')
    # def onchange_location_id(self):
    #     """
    #     根据选择的车辆，自动修改物理位置。
    #     默认位置为： virtual/（车牌号）
    #     :return:
    #     """
    #     if self.parent_vehicle:
    #         # inverntory 类型为虚拟库位
    #         location = self.parent_vehicle.mapped('location_id').filtered(lambda x: x.usage == 'inventory')
    #         if location:
    #             self.location_id = location
class StockMove(models.Model):
    _inherit = 'stock.move'

    component_id = fields.Many2one('product.component', string='Product Component')