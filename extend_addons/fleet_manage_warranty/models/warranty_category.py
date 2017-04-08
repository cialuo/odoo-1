# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Category(models.Model): # 保修类别
    _name = 'fleet_manage_warranty.category'
    _order = "idpath asc"

    name = fields.Char() # 名称
    code = fields.Char() # 代码

    idpath = fields.Char() # id路径

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

    manhour = fields.Float(digits=(6, 1), default=0 , compute='_compute_manhour') # 工时定额

    remark = fields.Char()  # 备注

    parent_id = fields.Many2one('fleet_manage_warranty.category', index=True, domain=[('state','=','in_use')]) # 父类
    child_ids = fields.One2many('fleet_manage_warranty.category', 'parent_id') # 子类

    items = fields.Many2many('fleet_manage_warranty.item', domain=[('state','=','in_use')]) # 保修项目 domain=[('type_tax_use','!=','none'), '|', ('active', '=', False), ('active', '=', True)],)

    sum_categories_manhour = fields.Float(digits=(6, 1), default=0, compute='_compute_manhour') # 子类工时汇总

    sum_items_manhour = fields.Float(digits=(6, 1), default=0, compute='_compute_manhour') # 项目工时汇总

    def category_manhour_get(self):
        result = []
        for record in self:
            sum_manhour = 0
            if record.child_ids:
                for child_record in record.child_ids:
                    sum_manhour += sum(child_record.items.mapped('manhour'))
                    print sum_manhour
                    sum_manhour += child_record.category_manhour_get()[0][1]
            result.append((record.id, sum_manhour))
        return result

    @api.depends('items', 'child_ids')
    def _compute_manhour(self):
        for category in self:
            temp_category_manhour=category.category_manhour_get()
            print temp_category_manhour
            category.sum_categories_manhour = category.category_manhour_get()[0][1]
            category.sum_items_manhour = sum(category.items.mapped('manhour'))
            category.manhour=category.sum_categories_manhour+category.sum_items_manhour

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.parent_id:
                name = "%s / %s" % (record.parent_id.name_get()[0][1], name)
            result.append((record.id, name))
        return result

    def idpath_get(self):
        result = []
        for record in self:
            idpath = record.id
            if record.parent_id:
                idpath = "%s/%s" % (record.parent_id.idpath_get()[0][1], idpath)
            result.append((record.id, idpath))
        return result

    @api.model
    def create(self, vals):
        result = super(Category, self).create(vals)
        idpath = "/" + str(result.idpath_get()[0][1]) + "/"
        result.idpath=idpath
        return result

    @api.multi
    def write(self, vals):
        idpath ="/"+str(self.idpath_get()[0][1])+"/"
        vals['idpath'] = idpath
        return super(Category, self).write(vals)
