# -*- coding: utf-8 -*-
{
    'name': "lty_dispatch_desktop",

    'summary': """
                            智能调度控制台""",

    'description': """
                            智能调度控制台
    """,

    'author': "jie.chen",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['dispatch_monitor_menu','lty_dispatch_desktop_base','lty_dispatch_jobs'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
}