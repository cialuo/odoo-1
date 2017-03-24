# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Category(models.Model): # 保修
    """
    """
    _name = 'fleet_manage_warranty.category'
    name = fields.Char() # 名称
    code = fields.Char() # 代码

    state = fields.Selection([ # 状态
        ('draft', "draft"),
        ('confirmed', "confirmed"),
        ('done', "done"),
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'


    # type = fields.Selection([ # 类型
    #     ('category', "分类"),
    #     ('item', "项目"),
    # ])

    # mode = fields.Selection([ # 保修方式
    #     ('inspect', "检查"),
    #     ('replace', "更换"),
    # ])

    manhour = fields.Float(compute='_compute_sum_manhour') # fields.Float(digits=(6, 2), help="工时定额") # 工时定额

    # remark = fields.Char()  # 备注
    remark = fields.Text()  # 备注

    # instructor_id = fields.Many2one('res.partner', string="Instructor")

    # parent_id = fields.Many2one('fleet_manage_warranty.warranty',
    #                             ondelete='cascade', string="Parent_id")

    # sub_ids = fields.One2many(
    #     'fleet_manage_warranty.warranty', 'parent_id', string="Sub_ids")

    # rel_warrantys = fields.Many2many('fleet_manage_warranty.warranty', string="Rel_warrantys")


    parent_id = fields.Many2one('fleet_manage_warranty.category',  index=True)
    child_ids = fields.One2many('fleet_manage_warranty.category', 'parent_id')

    items = fields.Many2many('fleet_manage_warranty.item')

    sum_categories_manhour = fields.Float(compute='_compute_sum_categories_manhour')

    sum_items_manhour = fields.Float(compute='_compute_sum_items_manhour')

    # sum_manhour = fields.Float(compute='_compute_sum_manhour')

    @api.depends('items.manhour')
    def _compute_sum_items_manhour(self):
        for category in self:
            category.sum_items_manhour = sum(category.items.mapped('manhour'))

    @api.depends('child_ids.manhour')
    def _compute_sum_categories_manhour(self):
        for category in self:
            category.sum_categories_manhour = sum(category.child_ids.mapped('manhour'))

    @api.depends('items.manhour','child_ids.manhour')
    def _compute_sum_manhour(self):
        for category in self:
            # category.sum_items_manhour = sum(category.items.mapped('manhour'))
            # category.sum_categories_manhour = sum(category.child_ids.mapped('manhour'))
            category.manhour = category.sum_items_manhour+category.sum_categories_manhour

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.parent_id:
                name = "%s / %s" % (record.parent_id.name_get()[0][1], name)
            result.append((record.id, name))
        return result

    @api.multi
    def return_action_to_open(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        bom_ids = []
        if self.items:
            for item in self.items:
                if item.bom_line_ids:
                    for bom in item.bom_line_ids:
                        # bom_dicts.append(bom)
                        bom_ids.append(bom.id)

                        # bom_dicts.append({
                        #     'name': bom.name if bom.name != '/' else bom.name
                        # })

        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('fleet_manage_warranty', xml_id)
            res.update(
                context=dict(self.env.context), # , default_vehicle_id=self.id
                domain=[('id', 'in', bom_ids)]
                #domain=[('vehicle_id', '=', self.id)]
            )
            return res
        return False