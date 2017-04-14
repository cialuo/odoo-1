# -*- coding: utf-8 -*-
{
    'name': "fleet_important_component",

    'summary': """
        重要部件""",

    'description': """
        重要部件
    """,
    'author': "He",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['important_product'],
    'data': [
        'views/important_roster_views.xml',
        'views/important_classification_views.xml',
        'views/important_detailed_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}