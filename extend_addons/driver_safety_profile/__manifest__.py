# -*- coding: utf-8 -*-
{
    'name': "驾驶员安全档案",

    'summary': """
        驾驶员安全档案
        """,

    'description': """
        驾驶员安全档案包含安全公里、违章记录、事故记录、超速记录
    """,

    'author': "XJM",

    'website': "http://www.lantaiyuan.com/",

    'category': 'Advanced Edition',

    'version': '1.0',

    'depends': ['security_manage_menu','employees', 'scheduling_parameters'],

    'data': [
        'data/sequence.xml',
        'views/driver_safety_profile_view.xml',
    ],

    'installable': True,

    'application': True,
}
