# -*- coding: utf-8 -*-
{
    'name': "安全管理菜单",

    'description': """
        安全管理顶级菜单及下面的一级菜单
    """,

    'author': "Chen",
    'website': "http://www.lantaiyuan.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}