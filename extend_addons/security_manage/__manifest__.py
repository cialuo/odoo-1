{
    'name': "安全管理",

    'summary': """
        安全管理
        """,

    'description': """
        1）维修生产安全
        2）消防安全
        3）安全检查设置
    """,

    'author': "Chen",
    'website': "http://www.lantaiyuan.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Optional Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'security_manage_menu'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sequence.xml',

        'views/menu_repair_view.xml',
        'views/repair_disease_views.xml',
        'views/repair_emergency_plan_views.xml',
        'views/repair_maintainer_train_views.xml',
        'views/repair_produce_map_views.xml',
        'views/repair_quality_views.xml',
        'views/repair_safety_manage_views.xml',
        'views/repair_site_views.xml',
        'views/repair_source_of_danger_views.xml',

        'views/menu_fire_view.xml',
        'views/fire_danger_source_views.xml',
        'views/fire_device_manage_views.xml',
        'views/fire_device_map_views.xml',
        'views/fire_plan_views.xml',

        'views/menu_security_view.xml',
        # 'views/security_check_item_views.xml',
        # 'views/security_check_table_views.xml',
        'views/security_archives_class_manage_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
}
# -*- coding: utf-8 -*-
