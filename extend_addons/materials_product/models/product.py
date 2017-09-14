# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, exceptions
from lxml import etree
from datetime import datetime
from odoo.tools.translate import _
from odoo.exceptions import ValidationError

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
    parent_id = fields.Many2one('product.product', string='Parent Product')
    inter_code = fields.Char(string='Inter Code')
    default_code = fields.Char(compute='_compute_default_code', search='_search_default_code')
    keeper_id = fields.Many2one('res.users', string='Keeper')
    shelf = fields.Char(string='Shelf')
    contract_price = fields.Float(string='Contract Price')
    tech_ids = fields.One2many('product.tech.info', 'product_id', string='Tec Info')
    categ_id = fields.Many2one('product.category', help="Select category", required=True)
    cost_method = fields.Char(compute='_compute_cost_method')
    auto_lot = fields.Boolean(string="Auto Lot", default=False)

    _sql_constraints = [
        ('code_parent_category_uniq',
         'unique (inter_code,categ_id)',
         u'同分类物资编码必须唯一')
    ]
    @api.model
    def create(self, vals):
        res = super(Product, self).create(vals)
        res.product_tmpl_id.write({'categ_id': res.categ_id.id})
        return res

    @api.one
    @api.depends('categ_id.property_cost_method')
    def _compute_cost_method(self):
        self.cost_method = self.categ_id.property_cost_method

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

    def _search_default_code(self, operator, value):
        """
        由于default_code 字段，之前的name search 方法不能筛选过滤产品。
        后期如果会影响效率，则可把default_code 加个 store=True,则无需另写 search方法
        :param operator: 
        :param value: 
        :return: 
        """
        ids = []
        self._cr.execute("""SELECT p.id FROM product_product p JOIN product_category c ON (c.id=p.categ_id) WHERE p.inter_code ILIKE %s OR c.code ILIKE %s """, ("%%%s%%" % value, "%%%s%%" % value))
        ids.extend([row['id'] for row in self._cr.dictfetchall()])
        # products = self.env['product.product'].search([], limit=100).filtered(lambda x: value in x.default_code)
        return [('id', 'in', ids)]

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
    product_id = fields.Many2one('product.product')
    compare1 = fields.Char(string='Compare1')
    compare2 = fields.Char(string='Compare2')
    parameter1 = fields.Char(string='parameter1')
    parameter2 = fields.Char(string='parameter2')
    description = fields.Text(string='Description')
    note = fields.Char(string='note')


class InventoryOverload(models.Model):

    _inherit = "stock.inventory"

    @api.multi
    def unlink(self):
        for item in self:
            if item.state != 'draft':
                raise ValidationError(_("can not deleted with not in draft state"))
        return super(InventoryOverload, self).unlink()