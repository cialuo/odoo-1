# -*- coding: utf-8 -*-
{
    'name': "假期与考勤",

    'summary': """
        假期与考勤""",

    'description': """
        假期与考勤
    """,

    'author': "深圳市蓝泰源信息技术股份有限公司",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Optional Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','employees','employees_menu','hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/leavesettings.xml',
        'views/leaveandcheckingin.xml',
        'views/leave.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}