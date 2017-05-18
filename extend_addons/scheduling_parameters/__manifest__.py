# -*- coding: utf-8 -*-
{
    'name': "调度参数设置",

    'description': """
        调度参数设置
    """,

    'summary': """
        调度参数设置
        """,

    'author': "youmy",
    'website': "http://www.lantaiyuan.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['operation_menu', 'employees'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/schedule_employee.xml',
        'views/schedule.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}