# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Important product',
    'version': '1.0',
    'category': 'xiao',
    'summary': 'important product',
    'description': """

     产品增加重要部件概念。
     重要部件会包含属性：
     1、适用车型；
     2、交旧领新；
     3、退役寿命；
     4、里程数；

    """,
    'data': [
        'views/product_view.xml',
    ],
    'depends': ['product', 'fleet', 'materials_manage'],
}