# -*- coding: utf-8 -*-
{
    'name': "营收管理",

    'description': """
        营收管理
    """,

    'summary': """
        营收管理
        """,

    'author': "youmy",
    'website': "http://www.lantaiyuan.com/",
    'category': 'Basic Edition',
    'version': '0.1',

    'depends': ['operation_menu', 'scheduling_parameters', 'vehicle_manage'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/revenue.xml',
    ],

    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
