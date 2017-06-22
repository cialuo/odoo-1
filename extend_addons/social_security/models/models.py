# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SocialSecurity(models.Model):

    _name = 'social.socialsecurity'

    employee_id = fields.Many2one('hr.employee', string='employee', default=None)

    # 摘要
    summary = fields.Text(string='summary')

    # 社保缴费银行
    bank = fields.Char(string='social security bank')

    # 缴费时间
    chargetime = fields.Date(string='charge time')

    # 缴费金额
    money = fields.Float(string='charge money')

    # 单位缴费
    money_company = fields.Float(string='money compay ')

    # 个人缴费
    money_employee = fields.Float(string='money employee')

    # 社保账户
    jobnumber = fields.Char(related='employee_id.socialsecurityaccount', string='employee socialsecurityaccount', readonly=True)

    # 身份证号
    id_card = fields.Char(related='employee_id.id_card', string='employee id_card', readonly=True)
