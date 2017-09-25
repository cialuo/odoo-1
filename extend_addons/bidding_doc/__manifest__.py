# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'招标文件',
    'version': '1.0',
    'category': 'Advanced Edition',
    'summary': 'Bidding Doc',
    'author': 'Xiao',
    'description': """
    bidding document
    """,
    'data': ['views/bidding_doc_view.xml', 'security/ir.model.access.csv'],
    'depends': ['base', 'materials_menu', 'purchase'],
    'application': True,
}