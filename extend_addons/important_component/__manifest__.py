# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '重要部件',
    'version': '1.0',
    'category': 'Optional Edition',
    'summary': '重要部件管理',
    'author': 'Xiao',
    'description': """
    重要部件管理
    """,
    'data': [
        'views/component_view.xml',
        'views/vehicle_component_view.xml',
    ],
    'depends': ['materials_product', 'vehicle_manage'],
    'application': True,
}