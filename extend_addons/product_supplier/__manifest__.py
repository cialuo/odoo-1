# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'报价单',
    'version': '1.1',
    'category': 'Basic Edition',
    'summary': u'报价单',
    'author': 'Xiao',
    'description': """
    
    1.1   调整菜单顺序
    """,
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/supplier_view.xml',
    ],
    'depends': ['base', 'materials_menu', 'hr', 'purchase'],
    'application': True,
}