# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '采购计划',
    'version': '1.5',
    'category': 'Advanced Edition',
    'summary': 'Purchase Plan',
    'author': 'Xiao',
    'description': """
    采购计划，根据采购计划，生成需求单进行补货
    1.4  修改供应商逻辑，默认为补货规则选择的供应商，可修改。
    1.5  采购计划默认排序 ID desc
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
        'web_duplicate_visibility',
    ],
    'application': True,
}