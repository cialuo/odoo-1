# -*- coding: utf-8 -*-
{
    'name': "fleet_manage_basic",

    'description': """
        车辆基础管理 包含车辆技术管理，维修工艺管理，保养工艺管理，定额管理
    """,

    'author': "Xiangll",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet_manage_fault','hr','fleet'],

    # always loaded
    'data': [
        # 'data/fleet_data.xml',
        'views/basic.xml',
        'views/fleet_view.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}