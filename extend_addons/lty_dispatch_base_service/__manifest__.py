# -*- coding: utf-8 -*-
{
    'name': "lty_dispatch_base_service",

    'summary': """
        Base api""",

    'description': """
        前端基础服务API
    """,

    'author': "He",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        #'scheduling_parameters',
        #'vehicle_manage',
        #'bus_schedule_plan',
        #'lty_dispatch_config',
        #'lty_dispatch_desktop_base',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'data/data.xml',
        #'views/menus.xml',
    ]

}