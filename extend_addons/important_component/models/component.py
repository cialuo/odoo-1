# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, exceptions
from lxml import etree
from datetime import datetime
from odoo.tools.translate import _

class Product(models.Model):
    _inherit = 'product.product'

    # is_important = fields.Boolean(string='Important', default=False)
    important_type = fields.Selection(selection_add=[('component', 'Component')])
    component_ids = fields.One2many('product.component', 'product_id', string='Component Info')
    # 要件类型
    classification_id = fields.Many2one('fleet.important_classification', 'classification_id')

    # 部件类型
    component_type = fields.Selection([('is_spare_parts', 'Spare Parts'), ('is_assembly', 'Assembly')],
                                      string='Component Type', default='is_spare_parts')

    # 零件列表
    parts_ids = fields.One2many('product.parts_list', 'product_id')

    @api.depends('qty_available')
    def _compute_number_of_libraries(self):
        """
             根据在手数量，计算出在库数量
             在库数量 = 在手数量 - 随车数量
        :return:
        """
        for product in self:
            # 取重要部件
            if product.important_type == 'component':
                domain = ['&', ('product_id', '=', product.id), ('parent_vehicle', '!=', None)]
                count = self.env['product.component'].search_count(domain)
                product.number_of_libraries = product.qty_available - count
        return self

    # 在库数量
    number_of_libraries = fields.Float('Number of Libraries', compute=_compute_number_of_libraries)

    @api.multi
    def write(self, vals):

        if vals.get('component_type') == 'is_spare_parts':
            if len(self.parts_ids) > 0:
                raise exceptions.UserError(_("There is part data, so it cannot be modified!"))

        result = super(Product, self).write(vals)

        return result

    @api.multi
    def write(self, vals):
        """
        取消特殊管理的同时，也要取消特殊管理类别，
        并删除特殊管理类别对应的清单。
        :param vals:
        :return:
        """
        res = super(Product, self).write(vals)
        com_obj = self.env['product.component']
        quant_obj = self.env['stock.quant']
        for p in self:
            if vals.get('is_important') == True:
                if (vals.get('important_type') or p.important_type)  == 'component':
                    domain = [('location_id.usage','=', 'internal'), ('product_id', '=', p.id)]
                    quants = quant_obj.search(domain)
                    for quant in quants:
                        for x in range(int(quant.qty)):
                            com_obj.create({
                                'product_id': p.id,
                                'location_id': quant.location_id.id,
                                'state': 'avaliable',
                            })
            if vals.get('is_important') == False:
                if p.component_ids:
                    # 已被车型加入到列表中的重要部件不能被修改
                    important_product = self.env['vehicle.model.product'].search([]).mapped('product_id')
                    if p in important_product:
                        raise exceptions.ValidationError(_('Important product be Added to model can not change to not important!'))
                    p.component_ids.write({'active': False})
        return res

class Component(models.Model):
    _name = 'product.component'
    _order = 'id desc'


    """
    重要部件清单信息
    """

    product_id = fields.Many2one('product.product', string='Product', required=True)
    code = fields.Char(string='Component Code', default='/')
    odometer = fields.Float(string='Odometer')
    location_id =fields.Many2one('stock.location', string='Location')
    state = fields.Selection([('avaliable', 'Avaliable'), ('waiting_repare', 'Waiting Repare'),
                              ('inuse', 'Inuse'), ('repareing', 'Repareing')],
                             default='inuse')
    checkout_date = fields.Date(string='Checkout Date')
    move_id = fields.Many2one('stock.move', string='Move lines')
    parent_vehicle = fields.Many2one('fleet.vehicle', string='Vehicle', ondelete='cascade')
    active = fields.Boolean(default=True)
    product_img = fields.Binary('product img', related='product_id.image_medium', store=False, readonly=True)

    product_name = fields.Char('product name', related='product_id.name', store=False, readonly=True)

    product_component_type = fields.Selection('product component type', related='product_id.component_type',
                                              store=False, readonly=True)

    product_inter_code = fields.Char('product inter code', related='product_id.default_code', store=False,
                                     readonly=True)

    odometer_progress = fields.Float(string='odometer progress', compute='_get_odometer_progress',store=True)

    @api.depends('odometer', 'product_id.lifetime')
    def _get_odometer_progress(self):
        for component in self:
            if component.product_id.lifetime > 0:
                component.odometer_progress = round(
                    100.0 * (component.product_id.lifetime - component.odometer) / component.product_id.lifetime, 2)
            else:
                component.odometer_progress = 0.0


    _sql_constraints = [('code_uniq', 'unique (code)', u"部件编码已存在，请重新生成")]

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

    @api.multi
    def name_get(self):
        return [(component.id, '%s %s' % (component.code, component.product_id.display_name))
                for component in self]


class fleet_important_component(models.Model):
    _name = 'fleet.important_classification'

    """
         新增要件分类表
    """

    name = fields.Char('classification_name', required=True)
    classification_no = fields.Char('classification_no', required=True)
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

    # 用于重要部件与零件列表之间的关联关系
    product_id = fields.Many2one('product.product')

    # 用于零件列表与物资之间的关联关系
    product_parts = fields.Many2one('product.product')

    parts_number = fields.Integer('parts_number', required=True)

    product_code = fields.Char('product code', related='product_parts.default_code', store=False, readonly=True)

    product_specifications = fields.Text('product specifications', related='product_parts.description', store=False,
                                         readonly=True)
