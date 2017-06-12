# -*- coding: utf-8 -*-
{
    'name': "报表",

    'summary': """
        数据报表
        """,

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.lantaiyuan.com/",
    #'category': 'Optional Edition',
    'category': '720',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_views.xml',
        'views/menus.xml',
    ],
    'qweb': ['static/src/xml/report.xml'],
    'application': True

}