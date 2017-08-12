# -*- coding: utf-8 -*-
{
    'name': "lty_dispatch_restful",

    'summary': """
        restful api""",

    'description': """
        调度网关通讯的restful风格
    """,

    'author': "He",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['scheduling_parameters'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/menus.xml',
    ]

}