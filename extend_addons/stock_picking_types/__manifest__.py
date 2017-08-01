# -*- coding: utf-8 -*-
{
    'name': "分拣类型",

    'summary': """
        """,
    'description': """
        领料管理、发料管理、退料管理、交旧领新
    """,
    'author': "He",
    'category': 'Basic Edition',
    'version': '1.2',
    'depends': ['materials_menu', 'stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/picking_types.xml',
        'views/materialout_view.xml',
        'views/material_view.xml',
        'views/older_old_view.xml',
        'views/return_material_view.xml',
        'views/internal_allocation_view.xml',
        'views/views.xml',

    ],
    'application': True,
}