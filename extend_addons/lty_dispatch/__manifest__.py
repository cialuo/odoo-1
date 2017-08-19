# -*- coding: utf-8 -*-
{
    'name': "lty_dispatch",

    'summary': """
        运营调度应用""",

    'description': """
        运营调度应用
    """,

    'author': "lihaihe",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'sequence': 1,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'bus_schedule_plan',
        'lty_dispatch_abnormal_monitor',
        'lty_dispatch_config',
        'lty_dispatch_desktop',
        'lty_dispatch_desktop_base',
        'lty_dispatch_desktop_widget',
        'lty_dispatch_jobs',
        'lty_dispatch_restful',
        'lty_operating_supply',
        'lty_operation_map_base',
        'lty_operation_plan',
        'lty_server_access',
        'revenue'        
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',     
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}