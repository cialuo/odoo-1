# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Invisible Menu',
    'version': '1.0',
    'category': 'Basic Version',
    'summary': 'invisble menu',
    'author': 'Xiao',
    'description': """
    """,
    'data': ['security/invisible_group.xml'],
    'depends': [
        'stock',
        'purchase',
        'account',
        'fleet',
        'project',
        'hr',
        'maintenance',
    ],
    'auto_install': True,
}