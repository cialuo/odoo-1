# -*- coding: utf-8 -*-
{
    'name': "energy_management",

    'summary': """
        包括：能源站、能源桩、库位、安全检查
       """,

    'description': """

    """,

    'author': "He",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['materials_manage','security_manage'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/energy_station_view.xml',
        'views/security_check_view.xml',
        'views/energy_pile_view.xml',
        'views/energy_usage_record_view.xml',
        'views/warehouse_location_view.xml',
        'views/menus_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}