# -*- coding: utf-8 -*-
{
    'name': "行车作业计划编制",

    'summary': """行车作业计划编制""",

    'description': """
        行车作业计划编制
    """,

    'author': "深圳市蓝泰源信息技术股份有限公司",
    'website': "http://www.lantaiyuan.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Basic Edition',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'scheduling_parameters', 'employees'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True
}