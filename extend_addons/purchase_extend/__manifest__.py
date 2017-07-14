# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '采购管理',
    'version': '1.1',
    'category': 'Basic Edition',
    'summary': '采购管理',
    'author': 'Xiao',
    'description': """
    采购管理
    """,
    'data': [
        'views/purchase_menu.xml',
    ],
    'depends': ['materials_menu', 'purchase'],
    'application': True,
}