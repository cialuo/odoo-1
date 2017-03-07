# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class Item(models.Model): # 保修项目
    """
    """
    _name = 'fleet_manage_warranty.item'
    name = fields.Char() # 项目名称
    code = fields.Char() # 项目编码

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

    mode = fields.Many2one('fleet_manage_warranty.mode', 'Mode', help='Current mode of the item', ondelete="set null") # default=_get_default_state,

    manhour = fields.Float(digits=(6, 2)) # 工时定额 , help="工时定额"

    # remark = fields.Char() # 备注

    remark = fields.Text(string='Remark')  # 备注

    # instructor_id = fields.Many2one('res.partner', string="Instructor")

    # parent_id = fields.Many2one('fleet_manage_warranty.warranty',
    #                             ondelete='cascade', string="Parent_id")

    # sub_ids = fields.One2many(
    #     'fleet_manage_warranty.warranty', 'parent_id', string="Sub_ids")

    # rel_warrantys = fields.Many2many('fleet_manage_warranty.warranty', string="Rel_warrantys")


    bom_line_ids = fields.One2many('fleet_manage_warranty.item.line', 'bom_id', 'BoM Lines', copy=True)

    # line_id = fields.Many2one('mrp.bom.line', string="Line")


class ItemLine(models.Model): # 用料清单
    _name = 'fleet_manage_warranty.item.line'
    _order = "sequence"
    _rec_name = "product_id"

    def _get_default_product_uom_id(self):
        return self.env['product.uom'].search([], limit=1, order='id').id

    product_id = fields.Many2one(
        'product.product', 'Product', required=True)


    sequence = fields.Integer(
        'Sequence', default=1,
        help="Gives the sequence order when displaying.")


    bom_id = fields.Many2one(
        'mrp.bom', 'Parent BoM',
        index=True, ondelete='cascade', required=True)


    product_qty = fields.Float(
        'Product Quantity', default=1.0,
        digits=dp.get_precision('Product Unit of Measure'), required=True)

    product_uom_id = fields.Many2one(
        'product.uom', 'Product Unit of Measure',
        default=_get_default_product_uom_id,
        oldname='product_uom', required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control")

    default_usage = fields.Char()  # 默认用量
    collar_cap = fields.Char()  # 领用上限
    applicable_carmodel = fields.Char()  # 试用车型
    remark = fields.Text(string='Remark')  # 备注


class FleetManageWarrantyMode(models.Model): # 保修方式
    _name = 'fleet_manage_warranty.mode'
    # _order = 'sequence asc'

    name = fields.Char(required=True)
    # sequence = fields.Integer(help="Used to order the note stages")

    _sql_constraints = [('warranty_mode_name_unique', 'unique(name)', 'Mode name already exists')]