# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '仓储管理',
    'version': '1.1',
    'category': 'Basic Edition',
    'summary': '仓储管理',
    'author': 'Xiao',
    'description': """
    仓储管理\n
    1.1: 修正补货规则中最大数量可以小于最小数量的问题
    """,
    'data': [
        'views/stock_menu.xml',
    ],
    'depends': ['materials_menu', 'stock'],
    'application': True,
}