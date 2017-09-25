# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '采购管理',
    'version': '1.4',
    'category': 'Basic Edition',
    'summary': '采购管理',
    'author': 'Xiao',
    'description': """
    
    采购管理
    
    1.1 
    
        1:增加批量勾选产品功能
        2:修正采购管理生成的入库单为草稿状态 
        
    1.2 
        1: 翻译--内部参考 修改为 供应商编码。
        2：增加 调查文件 字段（attachment）。替换 内部备注 page
        3：字段 备注 调整到视图 group 中。
        4：增加 该供应商supplier 产品信息统计 字段
        5：form 视图 button 增加 产品信息统计
        6：增加 该供应商 退货单统计字段
        7： form 视图 button 增加 退货单统计
        8：增加 类型 字段
        9：增加 供应商类型 表
        10： 增加 供应商类型菜单 至 物资管理 – 基础资料
    1.3
        1：修正 分拣单中的退货按钮 增加 采购员 权限组
    1.4
        1: 询价管理 和 采购管理合并
    """,
    'data': [
        'views/purchase_menu.xml',
        'wizard/multi_product_view.xml',
        'views/purchase_order_view.xml',
        'views/partner_view.xml',
        'views/picking_view.xml',
        'security/ir.model.access.csv',
    ],
    'depends': ['materials_menu', 'purchase', 'stock_picking_types'],
    'application': True,
}