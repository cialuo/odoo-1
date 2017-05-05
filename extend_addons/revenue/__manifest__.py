# -*- coding: utf-8 -*-
{
    'name': "revenue",

    'description': """
        营收管理
    """,

    'author': "youmy",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['operation_menu'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/revenue.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}