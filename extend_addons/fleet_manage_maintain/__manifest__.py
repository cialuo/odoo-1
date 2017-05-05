# -*- coding: utf-8 -*-
{
    'name': "fleet_manage_maintain",

    'description': """
        主要功能包括 维修管理的报修单，预检单，维修单，交接单，检验单
    """,

    'author': "Xiangll",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet_manage_fault','fleet_manage_vehicle','stock_picking_types'],

    # always loaded
    'data': [
        # 'security/maintain_security.xml',
        # 'security/ir.model.access.csv',
        "data/sequence.xml",
        'views/fleet_manage_inspect.xml',
        'views/maintain_view.xml',
        'views/repair_record.xml',


    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}