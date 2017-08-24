# -*- coding: utf-8 -*-
{
    'name': "社保与养老",

    'summary': """
        社保与养老""",

    'description': """
        社保与养老
        0.2
            附件名称修复
    """,

    'author': "深圳市蓝泰源信息股份有限公司",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Optional Edition',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'employees', 'employees_menu'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/socialsecurity.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
}