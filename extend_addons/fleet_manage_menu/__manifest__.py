# -*- coding: utf-8 -*-
{
    'name': "fleet_manage_menu",

    'description': """
        fleet manage menu 
    """,

    'author': "Xiangll",

    'category': 'Uncategorized',
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