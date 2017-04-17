# -*- coding: utf-8 -*-

{
    'name': 'important_product_repair_record',
    'version': '1.0',
    'category': 'lty',
    'summary': '重要部件管理',
    'author': 'Xiang',
    'description': """
    重要部件的维修记录
    """,
    'data': [
        'views/import_product_view.xml',
    ],
    'depends': ['fleet_manage_maintain', 'fleet_important_component'],
}