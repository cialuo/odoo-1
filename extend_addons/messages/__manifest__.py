# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'消息通知',
    'version': '1.0',
    'category': 'Basic Edition',
    'summary': '',
    'author': 'He',
    'description': """
    1.0  
         包含 手机短信
            　微信消息
    """,
    'data': [
        'views/sms_model_view.xml',
    ],
    'depends': ['hr'],
    'application': True,
}