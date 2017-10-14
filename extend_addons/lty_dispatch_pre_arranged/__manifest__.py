# -*- coding: utf-8 -*-
{
    'name': "pre-arranged planning",

    'summary': """
        pre-arranged planning""",

    'description': """
        调度及机器人-调度预案
    """,

    'author': "jianggenghua",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['lty_dispatch_solution', 'lty_dispatch_jobs'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/dispatch_pre_arranged_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}