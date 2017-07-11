# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'菜单隐藏功能',
    'version': '1.1',
    'category': 'Basic Edition',
    'summary': 'invisble menu',
    'author': 'Xiao',
    'description': """
    """,
    'data': ['security/invisible_group.xml', 'views/project_task_view.xml'],
    'depends': [
        'stock',
        'purchase',
        'account',
        'fleet',
        'project',
        'maintenance',
        'hr_holidays',
        'hr_payroll',
        'calendar',
    ],
    'auto_install': True,
    'application': True,
}