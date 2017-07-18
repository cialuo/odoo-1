# -*- coding: utf-8 -*-
{
    'name': "lty_dispatch_jobs",

    'summary': """
        调度作业""",

    'description': """
        调度作业
    """,

    'author': "lihaihe",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['dispatch_monitor_menu'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/dispatch_abnormal_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}