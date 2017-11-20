# -*- coding: utf-8 -*-
{
    'name': "lty_dispatch_test_init_data",

    'summary': """
        lty_dispatch_test_init_data""",

    'description': """
        调度系统测试基础数据初始化模块
    """,

    'author': "lihaihe",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'scheduling_parameters',
		'lty_park_gps_collect',
    ],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'wizard/sation_gps_collect_wizard.xml',
        'data/vehicle_yard.xml',
        #'views/menus.xml',
    ]

}