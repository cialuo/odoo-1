{
    'name': "公用权限组",

    'summary': """
        公用权限组
        """,
    'description': """
        a)维修保养公用权限组(司机，站务，车间维修，车间调度，车间质检)
    """,

    'author': "xiang",
    'website': "http://www.lantaiyuan.com/",

    'category': 'Basic Edition',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'data/vehicle_group.xml',
        'security/maintain_warranty_group.xml',
    ],
    'installable': True,
    'application': True
}
