# -*- coding: utf-8 -*-
{
    'name': "看板视图",

    'summary': """
    看板视图
    """,

    'description': """
        1.安全管理
        2.车辆管理
        3.人力资源
        4.物资管理
    """,

    'author': "深圳市蓝泰源信息技术股份有限公司",
    'website': "http://www.lantaiyuan.com/",
    'category': 'Basic Edition',
    'version': '1.0',
    'depends': ['base','employees','employees_menu','materials_menu','security_manage_menu','vehicle_manage_menu','board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/rule_data.xml',
        'views/dashboard_views.xml',
        'views/dashboard_setting.xml',
        'views/employees_dashboard.xml',
        'views/materials_dashboard.xml',
        'views/security_dashboard.xml',
        'views/vehicle_dashboard.xml',
        'views/dashboard_menus.xml',
        'data/dashboard_setting_data.xml',
    ],
    'installable': True,
    'application': True,
}
