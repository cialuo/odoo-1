# -*- coding: utf-8 -*-
{
    'name': "lty_server_access",

    'summary': """
                            平台接入
    """,

    'description': """
                        平台接入
    """,

    'author': "lihaihe",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','operation_menu'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/cloud_server_config.xml',
        'views/dsp_server_config.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}