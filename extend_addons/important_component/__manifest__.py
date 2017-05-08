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
        'data/component_data.xml',
        'views/component_view.xml',
        'views/vehicle_component_view.xml',
        'views/maintain_view.xml',
        'views/warranty_view.xml',
        'views/stock_move.xml',
        'views/important_roster_views.xml',
        'views/important_classification_views.xml',
        'views/important_detailed_views.xml',
        'views/repair_record_view.xml',

    ],
    'depends': ['vehicle_maintain', 'vehicle_manage', 'vehicle_warranty'],
    'application': True,
}