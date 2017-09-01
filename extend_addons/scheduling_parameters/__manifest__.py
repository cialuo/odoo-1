# -*- coding: utf-8 -*-
{
    'name': "运营资源",

    'description': """
        a) 区域管理
        b）道路管理
        c）站点管理
        d）线路管理
        e）施救车队
        f）线路地图制作
    """,

    'summary': """
        运营资源
        """,

    'author': "Xiang",
    'website': "http://www.lantaiyuan.com/",

    'category': 'Basic Edition',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['dispatch_monitor_menu', 'employees', 'schedule_dispatch_group'],

    # always loaded
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        #'views/template_view.xml',
        'views/schedule_employee.xml',
        'views/schedule.xml',
        'views/rescue_fleet.xml',
        #'views/line_map_production.xml',
    ],
    #'qweb': ['static/src/xml/*.xml'],

    'installable': True,
    'application': True,
    'auto_install': False,
}