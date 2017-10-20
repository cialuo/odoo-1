# -*- coding: utf-8 -*-
{
    'name': "lty_dispatch_move_v3",

    'summary': """
        Dispatch data move2v3""",

    'description': """
        调度数据(运营理程、非运营理程、考勤信息)迁移到V4
    """,

    'author': "lihaihe",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'leaveandcheckingin',
        'vehicle_manage',
        'operation_menu',
        #'lty_dispatch_config',
        #'lty_dispatch_desktop_base',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/view.xml',
        #'views/menus.xml',
    ]

}