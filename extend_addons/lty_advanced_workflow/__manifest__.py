# -*- coding: utf-8 -*-
{
    'name': "lty_advanced_workflow",

    'summary': """
        高级审批工作流""",

    'description': """
        高级审批工作流
    """,

    'author': "lihaihe",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['employees','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/approve_cfg.xml',
        'views/approve_center.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}