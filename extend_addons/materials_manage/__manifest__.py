# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '物资管理',
    'version': '1.0',
    'category': 'lty',
    'summary': '物资管理',
    'author': 'Xiao',
    'description': """
    物资管理，包含采购，仓储，领用，燃料，核算分析，基础资料
    """,
    'data': [
        'data/picking_type_data.xml',
        'views/materials_view.xml',
    ],
    'depends': ['purchase', 'stock'],
}