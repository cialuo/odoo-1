# -*- coding: utf-8 -*-
{
    'name': "库存预警",

    'summary': """
        """,

    'description': """
    """,

    'author': "He",
    'website': "http://www.lantaiyuan.com/",
    'category': 'Optional Edition',
    'version': '0.1',
    'depends': ['base','stock_extend'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_search_wizard.xml',
        'views/warning_report.xml',
        'views/menus.xml',
    ],
    'application': True

}