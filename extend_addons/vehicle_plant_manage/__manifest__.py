# -*- coding: utf-8 -*-
{
    'name': "维修厂管理",

    'description': """
        1）维修厂管理

    """,

    'author': "Xiang",
    'website': "",

    'category': 'Basic Edition',
    'version': '0.3.2',

    # any module necessary for this one to work correctly
    'depends': ['vehicle_manage_menu', 'employees', 'web_tree_no_open'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/view.xml',

    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}

