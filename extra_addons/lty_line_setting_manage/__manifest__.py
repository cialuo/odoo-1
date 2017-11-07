# -*- coding: utf-8 -*-
{
    'name': "线路参数设置",

    'summary': """
        线路参数设置
    """,

    'description': """
        线路参数设置：线路配置发布，线路属性，通用配置，站场配置，预设事件，卡类配置
    """,

    'author': "xiong",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/card.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
}