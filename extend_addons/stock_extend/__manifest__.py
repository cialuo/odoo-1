# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '仓储管理',
    'version': '1.0',
    'category': 'Basic Edition',
    'summary': '仓储管理',
    'author': 'Xiao',
    'description': """
    仓储管理
    """,
    'data': [
        'views/stock_menu.xml',
    ],
    'depends': ['materials_menu', 'stock'],
    'application': True,
}