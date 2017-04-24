# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '物资管理',
    'version': '1.0',
    'category': 'Basic Edition',
    'summary': '物资管理',
    'author': 'Xiao',
    'description': """
    物资管理
    """,
    'data': [
        'views/product_view.xml',
    ],
    'depends': ['materials_menu', 'stock', 'purchase', 'fleet'],
    'application': True,
}