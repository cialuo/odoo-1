# -*- coding: utf-8 -*-
{
    'name': "fleet_manage_warranty_maintain",

    'description': """
        主要功能包括车辆保养管理的计划单，保养单，交接单，检验单
    """,

    'author': "XJM",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','fleet_manage_menu'],

    # always loaded
    'data': [
         'views/warranty_plan_view.xml',
         'views/warranty_plan_sheet_view.xml',
         'views/warranty_maintain_sheet_view.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}