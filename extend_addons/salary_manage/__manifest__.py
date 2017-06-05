# -*- coding: utf-8 -*-
{
    'name': "薪资管理",

    'summary': """
        员工薪资管理""",

    'description': """
        员工薪资管理
    """,

    'author': "深圳市蓝泰源信息股份有限公司",
    'website': "http://www.yourcompany.com",

    'category': 'Optional Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'employees', 'hr_payroll', 'leaveandcheckingin'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/salary_manage.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
}