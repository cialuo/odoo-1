# -*- coding: utf-8 -*-
{
    'name': "设备管理",

    'description': """
        设备管理
    """,

    'author': "Xiang",

    'category': 'Optional Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['vehicle_maintain', 'maintenance'],

    # always loaded
    'data': [
        'data/maintain_delivery_sequence.xml',

        'views/equipment_view.xml',
        'views/vehicle_view.xml',
        'views/maintain_view.xml'
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}