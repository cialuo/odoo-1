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


class WorkInjury(models.Model):
    """
    工伤管理
    """

    _name = 'social.workinjury'

    def _applyUser(self):
        userid = self._uid
        users = self.env['hr.employee'].search([('user_id', '=', userid)])
        if len(users) != 0:
            return users[0].id
        else:
            return None

    employee_id = fields.Many2one('hr.employee', string='employee', default=_applyUser, required=True)

    # 性别
    sex = fields.Selection(related='employee_id.sex', string='employee sex', readonly=True)

    # 名称
    name = fields.Char(related='employee_id.name', string='employee name', readonly=True)

    # 出生日期
    birthday = fields.Date(related='employee_id.birthday', string='employee birthday', readonly=True)

    # 身份证号
    id_card = fields.Char(related='employee_id.id_card', string='employee id_card', readonly=True)

    # 职位
    workpost = fields.Many2one(related='employee_id.workpost', string='employee workpost', readonly=True)

    # 手机
    mobile_phone = fields.Char(related='employee_id.mobile_phone', string='employee mobile_phone', readonly=True)

    # 住址
    live_address = fields.Char(related='employee_id.live_address', string='employee live_address', readonly=True)

    # 部门
    department_id = fields.Many2one(related='employee_id.department_id', string='employee department', readonly=True)

    # 入职时间
    entrydate = fields.Date(related='employee_id.entrydate', string='employee entrydate', readonly=True)


    # 事故时间
    accidenttime = fields.Date(string="accidetn time", required=True)

    # 诊断时间
    checkingtime = fields.Date(string="checking time", required=True)

    # 受伤部位
    position = fields.Char(string="hurt position", required=True)

    # 职业病名称
    diseasename = fields.Char(string="disease's name")

    # 接触职业病危害岗位
    hurtpost = fields.Char(string="hurt post")

    # 接触职业病危害时间
    hurttime = fields.Date(string="hurt time")

    # 受伤害经过简述
    description = fields.Text(string="disease description")

    # 公司认定附件
    attachments = fields.Binary(string="checking attachments")

    # 状态
    state = fields.Selection([("draft", "draft"),                   # 草稿
                              ("reporting", "reporting"),           # 申报中
                              ], default='draft', string="work injury state ")

    # 状态
    state_checking_state = fields.Selection([("companychecking", "companychecking"),  # 公司认定
                                       ("socialchecking", "socialchecking"),    # 社保认定
                                       ("done", "done")                         # 社保认定
                                       ], default='companychecking', string="work injury checking state ")

    # 工伤鉴定图
    checkingimage = fields.Binary('injury checking report image')

    @api.multi
    def action_reporting(self):
        self.state= 'reporting'

    @api.multi
    def action_companychecking(self):
        self.state_checking_state = 'socialchecking'

    @api.multi
    def action_socialchecking(self):
        self.state_checking_state = 'done'
