# -*- coding: utf-8 -*-
{
    'name': "分拣类型",

    'summary': """
        """,
    'description': """
        领料管理、发料管理、退料管理、交旧领新
    """,
    'author': "He",
    'category': 'Warehouse',
    'version': '0.1',
    'depends': ['materials_manage'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/picking_types.xml',
        'views/views.xml',

    ],
    'demo': [
        # 'data/picking_types.xml',
    ],
    'application': True,
}