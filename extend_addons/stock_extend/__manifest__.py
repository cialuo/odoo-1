# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '仓储管理',
    'version': '1.2',
    'category': 'Basic Edition',
    'summary': '仓储管理',
    'author': 'Xiao',
    'description': """
    仓储管理;1.1: 修正补货规则中最大数量可以小于最小数量的问题,修正分拣类型只在草稿状态可改变;
    1.2: 修正仓库管理--仓库设置 ， 菜单调整至  基础资料
    """,
    'data': [
        'views/stock_menu.xml',
    ],
    'depends': ['materials_menu', 'stock', 'stock_picking_types'],
    'application': True,
}