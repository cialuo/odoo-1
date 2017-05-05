# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WarrantyCategory(models.Model): # 维保类别
    _name = 'warranty_category'
    _order = "idpath asc"

    name = fields.Char(string="Warranty Category Name") # 名称
    code = fields.Char(string='Warranty Category Code', required=True) # 代码

    idpath = fields.Char() # id路径
    level = fields.Integer() # 层级

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

    parent_id = fields.Many2one('warranty_category', index=True, domain=[('state','=','in_use')],readonly="true") # 父分类
    child_ids = fields.One2many('warranty_category', 'parent_id') # 子分类

    project_ids = fields.Many2many('warranty_project', domain=[('state','=','in_use')]) # 保修项目

    sum_categorie_manhour = fields.Float(digits=(6, 1), default=0, compute='_compute_manhour') # 子类工时汇总

    sum_project_manhour = fields.Float(digits=(6, 1), default=0, compute='_compute_manhour') # 项目工时汇总

    warranty_type = fields.Selection([ # 维保类型
        ('warranty', 'Warranty'),
        ('maintain', 'Maintain'),
        ], string="Warranty Type", default="warranty")

    warranty_level = fields.Many2one('warranty_level', 'Warranty Level', ondelete="set null") # 维保级别

    def category_manhour_get(self):
        result = []
        for record in self:
            sum_manhour = 0
            if record.child_ids:
                for child_record in record.child_ids:
                    sum_manhour += sum(child_record.project_ids.mapped('manhour'))
                    sum_manhour += child_record.category_manhour_get()[0][1]
            result.append((record.id, sum_manhour))
        return result

    @api.depends('project_ids', 'child_ids')
    def _compute_manhour(self):
        for category in self:
            # temp_category_manhour=category.category_manhour_get()
            category.sum_categorie_manhour = category.category_manhour_get()[0][1]
            category.sum_project_manhour = sum(category.project_ids.mapped('manhour'))
            category.manhour=category.sum_categorie_manhour+category.sum_project_manhour

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
        result = super(WarrantyCategory, self).create(vals)
        idpath = "/" + str(result.idpath_get()[0][1]) + "/"
        result.idpath=idpath
        result.level=idpath.count("/")-1
        return result

    @api.multi
    def write(self, vals):
        idpath ="/"+str(self.idpath_get()[0][1])+"/"
        vals['idpath'] = idpath
        vals['level'] = idpath.count("/")-1
        return super(WarrantyCategory, self).write(vals)
