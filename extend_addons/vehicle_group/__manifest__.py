{
    'name': "车辆管理 公用权限组",

    'summary': """
        公用权限组
        """,
    'description': """
        a)维修保养公用权限组(司机，站务，车间维修，车间调度，车间质检)
    """,

    'author': "Xiang",
    'website': "http://www.lantaiyuan.com/",

    'category': 'Basic Edition',
    'version': 'V0.3',

    'depends': ['base'],

    'data': [
        'data/vehicle_group.xml',
        'security/maintain_warranty_group.xml',
    ],
    'installable': True,
    'application': True
}
