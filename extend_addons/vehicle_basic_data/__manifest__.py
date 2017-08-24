# -*- coding: utf-8 -*-
{
    'name': "车辆基础数据",

    'description': """
        1、车辆品牌
        2、车辆类型
        3、故障分类
        4、故障现象
        5、故障原因
        6、维修方法
    """,

    'author': "He",
    'website': "",

    'category': 'Optional Edition',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['vehicle_maintain', 'vehicle_warranty', 'vehicle_manage'],

    # always loaded
    'data': [
        'data/vehicle_brand.xml',
        'data/vehicle_model.xml',
        'data/maintain_fault_category.xml',
        'data/maintain_fault_appearance.xml',
        'data/maintain_fault_reason.xml',
        'data/maintain_fault_method.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}