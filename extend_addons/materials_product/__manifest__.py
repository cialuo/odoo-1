# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '物资管理',
    'version': '1.1',
    'category': 'Basic Edition',
    'summary': '物资管理',
    'author': 'Xiao',
    'description': """
    物资管理
    """,
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'depends': ['materials_menu', 'stock', 'purchase', 'fleet'],
    'application': True,
}