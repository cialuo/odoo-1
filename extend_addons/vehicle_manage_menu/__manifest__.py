# -*- coding: utf-8 -*-
{
    'name': "车辆管理菜单",

    'description': """
        车辆管理菜单项
    """,

    'author': "Xiang",
    'website': "",

    'category': 'Basic Edition',
    'version': '0.3',

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