# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'报价单',
    'version': '1.0',
    'category': 'Basic Edition',
    'summary': u'报价单',
    'author': 'Xiao',
    'description': """
    
    
    """,
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/supplier_view.xml',
    ],
    'depends': ['base', 'materials_menu', 'hr', 'purchase'],
}