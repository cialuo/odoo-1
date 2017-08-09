# -*- coding: utf-8 -*-
{
    'name': "lty_dispatch_config",

    'summary': """
                            调度参数配置""",

    'description': """
                           1）运营管理/配置
                           2）调度监控/参数设置/通用配置
                           3）调度监控/参数设置/调度配置
    """,

    'author': "He",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['dispatch_monitor_menu','operation_menu'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menus.xml',
        'views/dispatch_setting_view.xml',
        'views/general_setting_view.xml',
        'views/operation_setting_view.xml',
    ],
}