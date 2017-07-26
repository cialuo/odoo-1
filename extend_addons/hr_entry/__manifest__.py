# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'入职离职管理',
    'version': '1.0',
    'category': 'Optional Edition',
    'summary': '',
    'author': 'Xiao',
    'description': """
    1.0 
        入职离职管理
    """,
    'data': [
        'views/hr_entry_view.xml',
        'security/ir.model.access.csv',
        # 'security/security.xml',
    ],
    'depends': ['employees'],
}