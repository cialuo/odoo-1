# -*- coding: utf-8 -*-
{
    'name': "vehicle_manage_menu",

    'description': """
        车辆管理菜单项
    """,

    'author': "Xiang",

    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
         'views/menu_view.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,    
}