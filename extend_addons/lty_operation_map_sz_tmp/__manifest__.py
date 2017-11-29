# -*- coding: utf-8 -*-
{
    'name': "lty_opertation_map_sz_tmp",

    'summary': """
        线路地图_终端版
    """,

    'description': """
        线路地图_终端版
    """,

    'author': "lk",
    'website': "http://www.lantaiyuan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web'],
    # 'depends': ['lty_dispatch_desktop_widget','scheduling_parameters','schedule_dispatch_group', 'dispatch_monitor_menu'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/line_map_production.xml',
        'views/template_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
	],
    'qweb': ['static/src/xml/*.xml'],		
}