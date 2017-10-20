# -*- coding: utf-8 -*-
{
    'name': "薪资管理",

    'summary': """
        员工薪资管理""",

    'description': """
        员工薪资管理
        0.2
            修正 打印工资信息 的权限组
    """,

    'author': "深圳市蓝泰源信息股份有限公司",
    'website': "http://www.yourcompany.com",

    'category': 'Optional Edition',
    'version': '0.2',


    # any module necessary for this one to work correctly
    'depends': ['base', 'employees', 'hr_payroll', 'leaveandcheckingin', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/salary_manage.xml',
        'views/hr_payroll_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
}