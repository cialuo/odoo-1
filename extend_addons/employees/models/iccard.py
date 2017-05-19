# -*- coding: utf-8 -*-

# ic卡管理

from odoo import models, fields, api, _
from datetime import datetime

class ICCard(models.Model):
    """
    IC卡
    """
    _name = 'employees.iccards'
    _rec_name = 'cardsn'

    _sql_constraints = [('card sn unique', 'unique (cardsn)', 'Card SN Can not duplication')]

    active = fields.Boolean('Active', default=True)
    # 卡号
    cardsn = fields.Char('card SN')
    # 状态
    status = fields.Selection([
        ('inactive','inactive'),    # 未启用
        ('active','active'),        # 启用
        ('loss','loss'),            # 挂失
        ('broken','broken'),        # 损坏
        ('blockup','blockup'),      # 停用
    ], string='status', default='inactive')
    # 员工
    employee_id = fields.Many2one('hr.employee', string='employee', default=None)
    # 启用日期
    active_date = fields.Date(string='active date')
    # 停用日期
    inactive_date = fields.Date(string='inactive date')
    # 停用原因
    inactive_reason = fields.Selection([
        ('loss','loss'),            # 挂失
        ('broken','broken'),        # 损坏
        ('inactive','inactive'),    # 停用
    ],string='inactive reason')
    # IC卡使用记录
    usage_records = fields.One2many('employees.iccards.usage', 'iccar_id', string='IC Card usage records')

    def toggle_active(self):
        self.inactive_date = datetime.today()
        return super(ICCard, self).toggle_active()

    @api.multi
    def returnCard(self):
        for item in self:
            if item.employee_id.id != False:
                record = [(0, _, {'user':item.employee_id.id,'returndate':datetime.today()})]
                item.write({'usage_records':record,'status':'inactive'})
        return True

class CardReturnRecords(models.Model):
    """
    IC卡使用记录
    """
    _name = 'employees.iccards.usage'

    iccar_id = fields.Many2one('employees.iccards', string='IC Card')
    # 使用人
    user = fields.Many2one('hr.employee', string='ic Card User')
    # IC卡归还日期
    returndate = fields.Date('IC Card return date')


class CardDispatchRecords(models.Model):
    _name = 'employees.iccards.dispatch'
    _rec_name = 'iccar_id'

    # 关联的ic卡
    iccar_id = fields.Many2one('employees.iccards', string='IC Card')
    # 领卡用户
    user = fields.Many2one('hr.employee', string='ic Card User')
    # 发卡时间
    dispatchtime = fields.Date('dispatch date', default=lambda self:datetime.today())
    # 发卡原因
    reason = fields.Char('dispatch reasion',)
    # 操作员
    operator = fields.Many2one('res.users', string='card dispatch operator', default=lambda self: self._uid)

    @api.model
    def create(self, vals):
        iccard = self.env['employees.iccards']
        cardinfo  = iccard.browse([vals['iccar_id']])
        if len(cardinfo) > 0 :
            ins = cardinfo[0]
            newdata = {}
            newdata['status'] = 'active'
            newdata['employee_id'] = vals['user']
            if ins.active_date == False:
                newdata['active_date'] = datetime.today()
            ins.write(newdata)
        res = super(CardDispatchRecords, self).create(vals)
        return res