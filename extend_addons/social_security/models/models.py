# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SocialSecurity(models.Model):
    """
    社保缴纳情况
    """

    _name = 'social.socialsecurity'

    employee_id = fields.Many2one('hr.employee', string='employee', default=None, required=True)

    # 摘要
    summary = fields.Text(string='summary')


    # 缴费时间
    chargetime = fields.Date(string='charge time', required=True)

    # 缴费金额
    money = fields.Float(string='charge money', compute="_totalChargeMoney")

    @api.onchange('money_company', 'money_employee')
    @api.multi
    def _totalChargeMoney(self):
        for item in self:
            item.money = item.money_company + item.money_employee

    # 单位缴费
    money_company = fields.Float(string='money compay', required=True)

    # 个人缴费
    money_employee = fields.Float(string='money employee', required=True)

    # 社保账户
    socialsecurityaccount = fields.Char(related='employee_id.socialsecurityaccount', string='employee socialsecurityaccount', readonly=True)

    # 身份证号
    id_card = fields.Char(related='employee_id.id_card', string='employee id_card', readonly=True)


class HousingProvident(models.Model):
    """
    公积金缴纳情况
    """

    _name = 'social.housingprovident'

    employee_id = fields.Many2one('hr.employee', string='employee', default=None, required=True)

    # 摘要
    summary = fields.Text(string='summary')


    # 缴费时间
    chargetime = fields.Date(string='charge time', required=True)

    # 缴费金额
    money = fields.Float(string='charge money', compute="_totalChargeMoney")

    @api.onchange('money_company', 'money_employee')
    @api.multi
    def _totalChargeMoney(self):
        for item in self:
            item.money = item.money_company + item.money_employee

    # 单位缴费
    money_company = fields.Float(string='money compay', required=True)

    # 个人缴费
    money_employee = fields.Float(string='money employee', required=True)

    # 社保账户
    socialsecurityaccount = fields.Char(related='employee_id.socialsecurityaccount', string='employee socialsecurityaccount',
                            readonly=True)

    # 身份证号
    id_card = fields.Char(related='employee_id.id_card', string='employee id_card', readonly=True)