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
 
 1: 盘点明细行视图增加 部件清单，m2m字段
 
 2： 当前产品为重要部件，部件清单加入默认值
 
 3： 盘盈
 
    1）： 盘盈库位---盘点库位 （库存移动）
    
    2）： 新建部件编号，状态  在库待用 （部件清单）
    
 4：盘亏
 
    1）：盘点库位---盘亏库位 （库存移动）
    
    2）：部件清单 active -- false
    
    """
    component_ids = fields.Many2many('product.component', 'inventory_line_componet_rel', 'line_id', 'component_id', string="Component")
