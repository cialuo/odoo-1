# -*- coding: utf-8 -*-
{
    'name': "设备管理",

    'description': """

    a）设备管理:
        1,设备管理
        2,设备分类
    b）车辆随车设备

    c）维修管理的交接单

    d)消防安全的消防设备管理
    """,

    'author': "Xiang",
    'website': "",

    'category': 'Optional Edition',
    'version': 'V0.3',

    # any module necessary for this one to work correctly
    'depends': ['vehicle_maintain', 'vehicle_warranty', 'maintenance','security_manage_menu','vehicle_group'],

    # always loaded
    'data': [
        'security/equipment_security.xml',
        'security/ir.model.access.csv',
        'data/maintain_delivery_sequence.xml',

        'views/equipment_view.xml',
        'views/vehicle_view.xml',
        'views/maintain_view.xml',
        'views/warranty_view.xml'
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}