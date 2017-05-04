# -*- coding: utf-8 -*-
{
    'name': "security_repair_produce",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'security_manage'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/repair_quality_views.xml',
        'views/repair_site_views.xml',
        'views/disease_views.xml',
        'views/emergency_plan_views.xml',
        'views/maintainer_train_views.xml',
        'views/produce_map_views.xml',
        'views/safety_manage_views.xml',
        'views/source_of_danger_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
