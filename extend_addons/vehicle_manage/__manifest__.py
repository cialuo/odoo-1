# -*- coding: utf-8 -*-
{
    'name': "车辆管理",

    'description': """
        a）车辆技术管理,车型管理,排放标准
        a）车辆使用档案,车辆生命周期,车辆年检管理
    """,

    'author': "Xiang,Tu,You",

    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet', 'vehicle_manage_menu', 'stock_extend', 'employees', 'scheduling_parameters'],

    # always loaded
    'data': [
        # 'data/fleet_data.xml',
        'views/vehicle_view.xml',
        'views/stock_location.xml',
        'views/fleetusagemanagement.xml',
        # 费用类型设置
        'views/cost_type_set.xml',
        # 车辆生命周期
        'views/vehicle_life_cycle.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}

