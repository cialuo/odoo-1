# -*- coding: utf-8 -*-
{
    'name': "油耗管理",

    'description': """
        车型管理中的油耗修正系数
    """,

    'author': "Xiang",
    'website': "",

    'category': 'Optional Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['energy_management'],

    # always loaded
    'data': [
        # 'data/fuel_data.xml',
        'views/fuel_view.xml',
        'views/fuel_consumption_update.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}