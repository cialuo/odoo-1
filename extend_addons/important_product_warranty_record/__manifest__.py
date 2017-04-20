# -*- coding: utf-8 -*-

{
    'name': 'important_product_warranty_record',
    'version': '1.0',
    'category': 'lty',
    'summary': '重要部件管理',
    'author': 'XJM',
    'description': """
        重要部件的保养记录
    """,
    'data': [
        'views/import_product_view.xml',
    ],
    'depends': ['fleet_manage_warranty_maintain', 'fleet_important_component'],
}