# -*- coding: utf-8 -*-
{
    'name': "fleet_manage_maintain",

    'description': """
        主要功能包括车辆维修管理的报修单，维修单，交接单，检验单
    """,

    'author': "Xiangll",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','fleet_manage_menu'],

    # always loaded
    'data': [
        'views/maintain_view.xml',
        "data/sequence.xml"
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}