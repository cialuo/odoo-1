# -*- coding: utf-8 -*-
{
    'name': "能源管理",

    'summary': """
        包括：能源站、能源桩、库位、安全检查
       """,

    'description': """

    """,

    'author': "He",
    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['materials_manage','security_manage','vehicle_manage'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/energy_station_view.xml',
        'views/security_check_view.xml',
        'views/energy_pile_view.xml',
        'views/energy_usage_record_view.xml',
        'views/warehouse_location_view.xml',
        'views/fleetusagemanagement.xml',
        'views/vehicle_view.xml',
        'views/menus_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'application': True
}