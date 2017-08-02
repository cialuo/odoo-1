# -*- coding: utf-8 -*-
{
    'name': "琛岃溅浣滀笟璁″垝缂栧埗",

    'summary': """
    琛岃溅浣滀笟璁″垝缂栧埗
    """,

    'description': """
        琛岃溅浣滀笟璁″垝缂栧埗
    """,

    'author': "娣卞湷甯傝摑娉版簮淇℃伅鎶�鏈偂浠芥湁闄愬叕鍙�",
    'website': "http://www.lantaiyuan.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Basic Edition',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','operation_menu', 'scheduling_parameters', 'employees', 'vehicle_manage'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'wizard/assigned_shifts.xml',
        'views/views.xml',
        'views/bus_date_type.xml',
        'views/bus_shift.xml',
        'views/bus_algorithm.xml',
        'views/bus_group.xml',
        'views/bus_staff_group.xml',
        'data/algorithm_data.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
}
