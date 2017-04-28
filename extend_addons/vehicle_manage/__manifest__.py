# -*- coding: utf-8 -*-
{
    'name': "车辆管理",

    'description': """
        a）车辆技术管理,车型管理,排放标准
    """,

    'author': "Xiang",

    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'fleet', 'vehicle_manage_menu','stock'],

    # always loaded
    'data': [
        # 'data/fleet_data.xml',
        'views/vehicle_view.xml',
        'views/stock_location.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}