# -*- encoding: utf-8 -*-
{
    'name': '登录界面',
    'description': """
        登录界面风格修改
    """,
    'version': '1.0',
    'category': 'Optional Edition',
    'author': "XJM",
    'website': 'http://www.lty.com',
    'license': 'AGPL-3',
    'depends': ['employees_menu'],
    'data': [
        'data/login_theme_data.xml',
        'data/ir_config_parameter.xml',
        'templates/webclient_templates.xml',
        'views/login_config_settings.xml',
    ],
    'qweb': [
        "static/src/xml/rw-web-menu.xml"
    ],
    'installable': True,
    'application': True,
}
