# -*- coding: utf-8 -*-
{
    'name': "fleet_manage_warranty",

    'description': """
        车辆管理 包含保修类别、子保修类别、保修项目
    """,

    'author': "Xiaojm",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','fleet_manage_menu'],

    # always loaded
    'data': [
         'views/warranty_category_view.xml',
         'views/warranty_item_view.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,    
}