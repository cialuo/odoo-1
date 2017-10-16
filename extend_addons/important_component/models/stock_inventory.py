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
from odoo import models, fields, api


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
        return {'type': 'ir.actions.act_window_close'}
    @api.multi
    def action_line_component(self):
        #打开当前明细行的部件清单
        action_ctx = dict(self.env.context)
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
    code = fields.Char(string="Component Code")
    product_id = fields.Many2one('product.product', string='Product')
    location_id = fields.Many2one('stock.location', string='Location')