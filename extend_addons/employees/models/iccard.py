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
    cardsn = fields.Char('card SN', copy=False, required=True)
    # 状态
    status = fields.Selection([
        ('inactive','inactive'),    # 未启用
        ('active','active'),        # 启用
        ('loss','loss'),            # 挂失
        ('broken','broken'),        # 损坏
        ('blockup','blockup'),      # 停用
    ], string='status', default='inactive')
    # 员工
    employee_id = fields.Many2one('hr.employee', string='employee', default=None, copy=False,ondelete='restrict')
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
                item.employee_id.iccard = False
                item.write({'usage_records':record,'status':'inactive'})
        return True

class CardReturnRecords(models.Model):
    """
    IC卡使用记录
    """
    _name = 'employees.iccards.usage'

    iccar_id = fields.Many2one('employees.iccards', string='IC Card', ondelete='cascade')
    # 使用人
    user = fields.Many2one('hr.employee', string='ic Card User')
    # IC卡归还日期
    returndate = fields.Date('IC Card return date')


class CardDispatchRecords(models.Model):
    _name = 'employees.iccards.dispatch'
    _rec_name = 'iccar_id'

    # 关联的ic卡
    iccar_id = fields.Many2one('employees.iccards', string='IC Card', ondelete='cascade')
    # 领卡用户
    user = fields.Many2one('hr.employee', string='ic Card User',domain=[('iccard','=',False)])
    # 发卡时间
    dispatchtime = fields.Date('dispatch date', default=fields.date.today)
    # 发卡原因
    reason = fields.Char('dispatch reasion',)
    # 操作员
    operator = fields.Many2one('res.users', string='card dispatch operator', default=lambda self: self._uid)

    @api.model
    def create(self, vals):
        iccard = self.env['employees.iccards']
        employee = self.env['hr.employee']
        user  = employee.browse([vals['user']])
        cardinfo  = iccard.browse([vals['iccar_id']])
        if len(cardinfo) > 0 :
            ins = cardinfo[0]
            newdata = {}
            newdata['status'] = 'active'
            newdata['employee_id'] = vals['user']
            if ins.active_date == False:
                newdata['active_date'] = datetime.today()
            ins.write(newdata)

        if user:
            user.write({'iccard':vals['iccar_id']})

        res = super(CardDispatchRecords, self).create(vals)
        return res

class certificate(models.Model):
    """
    特种工证照
    """
    _name = 'employees.certificate'

    # 证件名称
    name = fields.Char('certificate name', required=True)
    # 过期日期
    expiredate = fields.Date('certificate expire date')

    # 图片
    image = fields.Binary('certificate image')
    # 工号
    jobnumber = fields.Char(related='employee_id.jobnumber', readonly=True)
    # 用户名
    username = fields.Char(related='employee_id.name', readonly=True)
    # 岗位
    workpost = fields.Many2one(related='employee_id.workpost', readonly=True)
    # 员工状态
    employeestate = fields.Selection(related='employee_id.employeestate', readonly=True)

    # 用户图片
    userimage = fields.Binary(related='employee_id.image', readonly=True)

    # 关联员工
    employee_id = fields.Many2one('hr.employee', string='employee', default=None)
    # 部门
    department_id = fields.Many2one(related='employee_id.department_id', readonly=True)
    # 职称
    title = fields.Char(related='employee_id.title', readonly=True)
    # 电话
    mobile_phone = fields.Char(related='employee_id.mobile_phone', readonly=True)
    # 邮箱
    work_email = fields.Char(related='employee_id.work_email', readonly=True)