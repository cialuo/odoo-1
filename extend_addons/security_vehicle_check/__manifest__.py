# -*- coding: utf-8 -*-
{
    'name': "车辆安全检查",

    'description': """
        车辆安全检查
    """,

    'author': "hu wei",

    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['security_manage_menu', 'vehicle_manage','vehicle_group','materials_product','web_tree_no_open'],

    # always loaded
    'data': [
        'security/security_check.xml',
        'security/ir.model.access.csv',
        'data/check_default_data.xml',
        'views/views.xml',
        'views/security_check_item_views.xml',
        'views/security_check_table_views.xml',
        'views/vehicle_front_check_views.xml',
        'views/vehicle_everyday_check_views.xml',
        'views/vehicle_special_check_views.xml',
        'views/vehicle_abarbeitung_check_views.xml',
        'views/vehicle_detection_check_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
