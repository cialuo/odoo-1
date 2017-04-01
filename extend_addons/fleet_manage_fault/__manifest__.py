# -*- coding: utf-8 -*-
{
    'name': "fleet_manage_fault",

    'description': """
        主要功能包括：
        1,故障分类
        2,故障原因
        3,故障现象
        4,维修办法
        5,维修工艺管理
        6,定额管理
    """,

    'author': "Xiangll",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['product', 'hr', 'stock','fleet_manage_menu'],

    # always loaded
    'data': [
        'data/fault_maintain_type.xml',
        'views/fault_view.xml',
        'views/basic.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,    
}