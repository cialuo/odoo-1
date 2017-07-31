# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'物资基础数据',
    'version': '1.0',
    'category': 'Basic Edition',
    'summary': '',
    'author': 'Xiao',
    'description': """
    1.0  
         包含 物资计量单位数据
              物资分类数据
              物资数据
    """,
    'data': [
        'data/product.uom.csv',
        'data/product.category.csv',
        'data/product.product.csv',
    ],
    'depends': ['materials_product'],
}