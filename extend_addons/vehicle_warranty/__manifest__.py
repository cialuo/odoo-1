# -*- coding: utf-8 -*-
{
    'name': "维保模块",
    'description': """
        维保模块 包含车辆维保管理、维保体系
    """,
    'author': "XJM",
    'category': 'Advanced Edition',
    'version': '1.0',

    'depends': ['employees', 'vehicle_manage','materials_product','stock_picking_types'], # 'product','stock'
    'data': [
        'data/vehicle_warranty_data.xml',
        'views/warranty_category_view.xml',
        'views/warranty_project_view.xml',
        'views/warranty_plan_view.xml',
        'views/warranty_plan_order_view.xml',
        'views/warranty_order_view.xml',
        'views/warranty_interval_view.xml',
        'views/vehicle_warranty_record.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}