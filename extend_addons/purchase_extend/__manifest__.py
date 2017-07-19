# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '采购管理',
    'version': '1.1',
    'category': 'Basic Edition',
    'summary': '采购管理',
    'author': 'Xiao',
    'description': """
    采购管理
    1.1 1:增加批量勾选产品功能
        2:修正采购管理生成的入库单为草稿状态
    """,
    'data': [
        'views/purchase_menu.xml',
        'wizard/multi_product_view.xml',
        'views/purchase_order_view.xml',
    ],
    'depends': ['materials_menu', 'purchase'],
    'application': True,
}