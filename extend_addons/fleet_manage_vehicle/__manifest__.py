# -*- coding: utf-8 -*-
{
    'name': "fleet_manage_vehicle",

    'description': """
        车辆基础管理 包含车辆技术管理,车型管理
    """,

    'author': "Xiangll",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','fleet','fleet_manage_menu'],

    # always loaded
    'data': [
        # 'data/fleet_data.xml',

        'views/fleet_view.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}