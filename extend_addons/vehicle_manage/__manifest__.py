# -*- coding: utf-8 -*-
{
    'name': "车辆管理",

    'description': """
        1）车辆技术管理,车型管理,排放标准
        2）车辆使用档案,车辆生命周期,车辆年检管理
    """,

    'author': "Xiang,Tu,You,He V0.4",
    'website': "",

    'category': 'Basic Edition',
    'version': '0.4.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet', 'vehicle_manage_menu', 'stock_extend', 'employees',
                'scheduling_parameters','materials_product','vehicle_group'],

    # always loaded
    'data': [
        # 'data/fleet_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/vehicle_view.xml',
        'views/stock_location.xml',
        'views/fleetusagemanagement.xml',
        # 费用类型设置
        'views/cost_type_set.xml',
        # 车辆生命周期
        'views/vehicle_life_cycle.xml',
        'views/vehicle_config_settings_view.xml',
        'views/vehicle_entry_view.xml',
        'data/vehicle_brand.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}

