# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '采购计划',
    'version': '1.0',
    'category': 'Advanced Edition',
    'summary': 'Purchase Plan',
    'author': 'Xiao',
    'description': """
    采购计划，根据采购计划，生成需求单进行补货
    """,
    'data': [
        'data/purchase_plan.xml',
        # 'security/purchase_plan_security.xml',
        'security/ir.model.access.csv',
        'views/purchase_plan_view.xml',
    ],
    'depends': [
        'materials_product',
        'hr',
    ],
    'application': True,
}