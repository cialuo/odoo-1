# -*-coding:UTF-8-*-

{
    'name': "运营-调度 公用权限组",

    'summary': """
        运营-调度 公用权限组
        """,
    'description': """
        a)运营-调度 公用权限组(运营专员，运营经理，调度员，调度经理)
    """,

    'author': "Xiang",
    'website': "http://www.lantaiyuan.com/",

    'category': 'Basic Edition',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'data/schedule_dispatch_group.xml',
        'security/schedule_dispatch_group.xml',
    ],
    'installable': True,
    'application': True
}
