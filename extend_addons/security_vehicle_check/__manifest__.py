# -*- coding: utf-8 -*-
{
    'name': "security_vehicle_check",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "hu wei",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Basic Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'security_manage'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/vehicle_front_check_views.xml',
        'views/vehicle_everyday_check_views.xml',
        'views/vehicle_special_check_views.xml',
        'views/vehicle_abarbeitung_check_views.xml',
        'views/vehicle_detection_check_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
