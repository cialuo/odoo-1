# -*- coding: utf-8 -*-
{
    'name': "调度监控菜单",

    'description': """
        调度监控菜单
    """,

    'summary': """
        调度监控菜单
        """,

    'author': "Xiang",
    'website': "http://www.lantaiyuan.com/",

    'category': 'Basic Edition',
    'version': '0.1',


    'depends': ['base'],


    'data': [
        # 'security/ir.model.access.csv',
        'views/dispatch_monitor_menu.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
