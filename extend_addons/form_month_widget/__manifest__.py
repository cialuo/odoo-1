# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Month widget ',
    'version': '1.0',
    'category': 'Xiao',
    'summary': 'Widget',
    'author': 'Xiao',
    'description': """
    月度选择器
    """,
    'data': [
        'views/template.xml',
    ],
    'depends': [
        'web',
    ],
    'qweb': ['static/src/xml/form_month_widget.xml'],
}