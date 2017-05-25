# -*- coding: utf-8 -*-
{
    'name': "调度参数",

    'description': """
        调度参数
    """,

    'summary': """
        调度参数
        """,

    'author': "youmy",
    'website': "http://www.lantaiyuan.com/",

    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['operation_menu', 'employees'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/schedule_employee.xml',
        'views/schedule.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}