# -*- coding: utf-8 -*-
{
    'name': "lty_sataion_gps_collect",

    'summary': """
        station gps info collect""",

    'description': """
        站点GPS数据采集模块
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
    ],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'wizard/sation_gps_collect_wizard.xml',
        'views/view.xml',
        #'views/menus.xml',
    ]

}