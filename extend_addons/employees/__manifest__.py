# -*- coding: utf-8 -*-
{
    'name': "人力资源",

    'summary': """
    人力资源
        """,

    'description': """
        人力资源
    """,

    'author': "深圳市蓝泰源信息技术股份有限公司",
    'website': "http://www.lantaiyuan.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Basic Edition',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web_duplicate_visibility', 'hr', 'hr_contract', 'employees_menu'],

    # always loaded
    'data': [
        'security/security.xml',
        'data/transfer_number.xml',
        'security/ir.model.access.csv',
        'security/transfer/ir.model.access.csv',
        'views/ltyhr_employee_document.xml',
        'views/lty_groups.xml',
        'views/iccardmanage.xml',
        'views/experiencemanagement.xml',
        'views/assets.xml',
        'views/transfer.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True
}
