# -*- coding: utf-8 -*-
{
    'name': "vehicle_warranty",
    'description': """
        维保模块 包含车辆维保管理、维保体系
    """,
    'author': "XJM",
    'category': 'Advanced Edition',
    'version': '0.1',
    'depends': ['vehicle_manage_menu','product'],
    'data': [
        'views/warranty_category_view.xml',
        'views/warranty_item_view.xml',
        'views/warranty_plan_view.xml',
        'views/warranty_plan_order_view.xml',
        'views/warranty_order_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}