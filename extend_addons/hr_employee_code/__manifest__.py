# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': u'员工编码规则',
    'version': '1.0',
    'category': 'Optional Edition',
    'summary': '',
    'author': 'Xiao',
    'description': """
    1.0
        1：三级编码： （岗位编码，位数：2）（部门编码，位数：2） （员工工号，位数：5）
        2：部门 增加 编码 字段
        3： 岗位职能 增加 选项：管理 安保。
        4：岗位 增加 编码 字段，不验证唯一性
    """,
    'data': ['views/hr_employee_view.xml'],
    'depends': ['employees'],
}