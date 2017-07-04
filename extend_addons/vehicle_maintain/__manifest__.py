# -*- coding: utf-8 -*-
{
    'name': "抢修模块",

    'description': """
    a）抢修体系:
        1,故障分类
        2,故障原因
        3,故障现象
        4,维修办法
        5,维修工艺管理
        6,定额管理
    b）维修管理:
        1,报修单
        2,预检单
        3,维修单
        4,交接单
        5,检验单
    """,

    'author': "Xiang",
    'website': "",

    'category': 'Advanced Edition',
    'version': '0.3.1',

    # any module necessary for this one to work correctly
    'depends': ['vehicle_manage', 'materials_product',
                'stock_picking_types','vehicle_group',
                'web_tree_no_open',],

    # always loaded
    'data': [
        'security/maintain_security.xml',
        'security/ir.model.access.csv',

        'views/fault_view.xml',

        "data/maintain_sequence.xml",
        'views/maintain_inspect_view.xml',

        "views/maintain_view.xml",
        'views/vehicle_repair_record.xml',
        'views/vehicle_anchor.xml',
        'views/maintain_repair_calc.xml',

    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}