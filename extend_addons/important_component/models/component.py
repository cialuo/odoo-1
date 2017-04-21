# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, exceptions
from lxml import etree
from datetime import datetime
from odoo.tools.translate import _

class Product(models.Model):
    _inherit = 'product.product'

    is_important = fields.Boolean(string='Important', default=False)
    important_type = fields.Selection([('equipment', 'Equipment'), ('component', 'Component'), ('energy', 'Energy')],
                                      string='Important Type')
    component_ids = fields.One2many('product.component', 'product_id', string='Component Info')

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

    product_id = fields.Many2one('product.product', string='Product')
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

    @api.multi
    def name_get(self):
        return [(component.id, '%s %s' % (component.code, component.product_id.display_name))
                for component in self]