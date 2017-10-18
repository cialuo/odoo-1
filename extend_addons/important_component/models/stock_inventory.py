# -*- coding: utf-8 -*-
##############################################################################
#
#
#    Copyright (C) 2017 xiao (715294035@qq.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.
#
##############################################################################
from odoo import models, fields, api, exceptions

class Inventory(models.Model):
    _inherit = 'stock.inventory'

    @api.multi
    def prepare_inventory(self):
        """
        重写开始盘点。需要为每行属于重要部件的明细生成部件清单
        :return: 
        """
        res = super(Inventory, self).prepare_inventory()
        for order in self:
            #筛选重要部件的明细行,并增加该重要部件的需盘点明细编号
            components_line = order.line_ids.filtered(lambda x: x.product_id.is_important and x.product_id.important_type == 'component')
            for line in components_line:
                components = line.product_id.component_ids.filtered(lambda x: x.location_id == line.location_id)
                components_data = []
                for c in components:
                    vals = {
                        'code': c.code,
                        'product_id': line.product_id.id,
                        'component_id': c.id,
                        'type': 'in_loc',
                    }
                    components_data.append((0,0,vals))
                line.write({'component_ids': components_data})
        return res
    @api.multi
    def action_done(self):
        """
        明细行中的重要部件清单，增加的明细，则增加库存移动
        # 修改了部件编号，则直接修改重要部件编号
        :return: 
        """
        move = self.env['stock.move']
        component_obj = self.env['product.component']
        # res = super(Inventory, self).action_done()
        for order in self:
            components_line = order.line_ids.filtered(
                lambda x: x.product_id.is_important and x.product_id.important_type == 'component')
            if any([i.product_qty != len(i.component_ids.filtered(lambda x: x.type != 'loss')) for i in components_line if i.product_qty > 0]):
                raise exceptions.UserError(u"部件清单数量与实际数量不符")
            else:

                for line in components_line:
                    #需新增库存移动的部件清单
                    new_to_move = line.component_ids.filtered(lambda x: not x.type=='income')
                    #新增库存移动，重要部件
                    for component in new_to_move:

                        component_vals = {
                            'product_id': line.product_id.id,
                            'code': component.code,
                            'location_id': line.location_id.id,
                            'state': 'avaliable',
                            'move_id': move.id,
                        }
                        new_component = component_obj.create(component_vals)
                        move.write({'origin': new_component.code})
            # first remove the existing stock moves linked to this inventory
            order.mapped('move_ids').unlink()
            for normal_line in (order.line_ids - components_line):
                # compare the checked quantities on inventory lines to the theorical one
                stock_move = normal_line._generate_moves()
        self.write({'state': 'done'})
        self.post_inventory()
        return True



class InventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    """
 增加重要部件的盘点逻辑
 
 1: 盘点明细行视图增加 部件清单，o2m字段
 
 2： 当前产品为重要部件，部件清单加入默认值
 
 3： 盘盈
 
    1）： 盘盈库位---盘点库位 （库存移动）
    
    2）： 新建部件编号，状态  在库待用 （部件清单）
    
 4：盘亏
 
    1）：盘点库位---盘亏库位 （库存移动）
    
    2）：部件清单 active -- false
    
 5： 数量正确，编号不正确
 
    
    """
    component_ids = fields.One2many('inventory.line.component', 'line_id', string="Component")
    component_visible = fields.Boolean(compute='_compute_component_visible')

    @api.multi
    def _compute_component_visible(self):
        #计算当前明细行是否要显示部件清单
        for line in self:
            if line.product_id.is_important and line.product_id.important_type == 'component':
                line.component_visible = True
    @api.multi
    def save(self):
        """
        修改当前明细行的实际数量，等于 部件清单的数量
        :return: 
        """
        self.ensure_one()
        self.write({'product_qty': len(self.component_ids)})
        return {'type': 'ir.actions.act_window_close'}
    @api.multi
    def action_line_component(self):
        #打开当前明细行的部件清单
        action_ctx = dict(self.env.context)
        # action_ctx.update(
        # )
        view_id = self.env.ref('important_component.view_component_inventory_line').id
        return {
            'name': u'部件清单',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.inventory.line',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
            'res_id': self.ids[0],
        }

class LineComponent(models.Model):
    _name = 'inventory.line.component'

    line_id = fields.Many2one('stock.inventory.line', string='inventory line')
    code = fields.Char(string="Component Code", required=True)
    qty = fields.Integer(string='Qty', default=1)
    product_id = fields.Many2one('product.product', string='Product')
    component_id = fields.Many2one('product.component', string='Product Component')
    type = fields.Selection([('in_loc', 'In location'), ('loss', 'Loss'), ('income', 'Income')], default='income')
    # move_ids = fields.One2many('stock.move', 'line_componet_id', string='Stock move')