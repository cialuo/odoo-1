# -*- coding: utf-8 -*-
{
    'name': "能源管理",

    'summary': """
        能源管理
       """,

    'description': """

    """,

    'author': "He",
    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['materials_product','security_vehicle_check','vehicle_manage','vehicle_group','stock_warning'],

    # always loaded
    'data': [
        'security/energe_security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/energy_station_view.xml',
        'views/security_check_view.xml',
        'views/energy_pile_view.xml',
        'views/energy_usage_record_view.xml',
        'views/warehouse_location_view.xml',
        'views/fleetusagemanagement.xml',
        'views/vehicle_view.xml',
        'views/product.xml',
        'views/menus_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'application': True
}