# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime


class UnitTransfer(models.Model):
    """
     内部调动
     """
    _name = 'employees.innertransfer'

    # 调动单编码
    name = fields.Char(string="employees_transfer_code", required=True, index=True, default='/', readonly=True,
                       states={'draft': [('readonly', False)]})

    def _applyUser(self):
        userid = self._uid
        users = self.env['hr.employee'].search([('user_id', '=', userid)])
        if len(users) != 0:
            return users[0].id
        else:
            return None

    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade', default=_applyUser, readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 员工工号
    jobnumber = fields.Char(related='employee_id.jobnumber', string='employee jobnumber', readonly=True)

    # 创建时间
    create_date = fields.Datetime(string='create time', default=lambda self: datetime.now(), readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 制表人
    create_user = fields.Many2one('res.users', string='create user', default=lambda self: self._uid, readonly=True,
                                  states={'draft': [('readonly', False)]})

    def _defaultpost(self):
        userid = self._uid
        users = self.env['hr.employee'].search([('user_id', '=', userid)])
        if len(users) != 0:
            return users[0].workpost.id
        else:
            return None

    # 原岗位
    original_post = fields.Many2one('employees.post', ondelete='restrict',
                                    string="employees_original_post", default=_defaultpost, readonly=True,
                                    states={'draft': [('readonly', False)]})

    def _defaultdepartment(self):
        userid = self._uid
        users = self.env['hr.employee'].search([('user_id', '=', userid)])
        if len(users) != 0:
            did = users[0].department_id.id
            return did
        else:
            return None

    # 原部门
    original_section = fields.Many2one('hr.department', ondelete='restrict',
                                       string="employees_original_section", default=_defaultdepartment)

    # 新单位岗位
    new_post = fields.Many2one('employees.post', ondelete='restrict', string="employees_new_post", readonly=True,
                               states={'draft': [('readonly', False)]})
    # 新部门
    new_section = fields.Many2one('hr.department', string="employees_new_section", readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 状态
    state = fields.Selection([("draft", "employees_unit_draft"),  # 草稿
                              ("confirmed", "employees_unit_confirmed"),  # 待审批
                              ("done", "employees_unit_done"),  # 已完成
                              ], default='draft', string="employees_unit_status")

    def _defaultType(self):
        type = self._context.get('transtype', False)
        if type == 'unit':
            return 'unit'
        elif type == 'post':
            return 'post'

    @api.onchange('employee_id')
    def _changeRelatedField(self):
        employeeInfo = self.env['hr.employee'].browse([self.employee_id.id])
        if len(employeeInfo) > 0:
            employeeInfo = employeeInfo[0]
            self.original_post = employeeInfo.workpost.id
            self.original_section = employeeInfo.department_id.id

    # 调动类型
    transfer_type = fields.Selection([
        ('unit', 'unit transfer'),  # 单位调动
        ('post', 'post transfer')  # 岗位调动
    ], string='tranfer type', default=_defaultType, index=True, readonly=True,
        states={'draft': [('readonly', False)]})

    # 调动原因
    transfer_reason = fields.Text(string="employees_transfer_reason", readonly=True,
                                  states={'draft': [('readonly', False)]})
    # 审批/会签人员
    countersign_person = fields.Many2many('hr.employee', string="employees_countersign_person", readonly=True,
                                          states={'draft': [('readonly', False)]})

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr_employees.transfer') or '/'
        employeeid = vals.get('employee_id')
        employeeInfo = self.env['hr.employee'].browse([employeeid])
        if len(employeeInfo) > 0:
            employeeInfo = employeeInfo[0]
            vals['original_post'] = employeeInfo.workpost.id
            vals['original_section'] = employeeInfo.department_id.id
        return super(UnitTransfer, self).create(vals)

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        record = {
            'name': self.name,
            'transferdate': self.create_date,
            'employee_id': self.employee_id.id,
            'original_unit': self.original_section.name,
            'original_post': self.original_post.name,
            'new_section': self.new_section.name,
            'new_post': self.new_post.name,
            'transfer_reason': self.transfer_reason,
        }
        if self.transfer_type == 'unit':
            record['transfer_type'] = 'unit_transfer'
        elif self.transfer_type == 'post':
            record['transfer_type'] = 'post_transfer'
        recins = self.env['employees.transfer.record'].create(record)
        countersign_person = []
        for item in self.countersign_person:
            countersign_person.append((4, item.id,))
        recins.write({'countersign_person': countersign_person})
        self.employee_id.write({'department_id': self.new_section.id, 'workpost': self.new_post.id})
        self.state = 'done'

    @api.multi
    def unlink(self):
        for order in self:
            if not order.state == 'draft':
                raise exceptions.UserError(_('only delete in state draft'))
        return super(UnitTransfer, self).unlink()


class ForeignTransfer(models.Model):
    """
    对外调动
    """
    _name = 'employees.foreign'

    # 调动单编码
    name = fields.Char(string="employees_transfer_code", index=True, copy=False, default='/', readonly=True,
                       states={'draft': [('readonly', False)]})
    def _applyUser(self):
        userid = self._uid
        users = self.env['hr.employee'].search([('user_id', '=', userid)])
        if len(users) != 0:
            return users[0].id
        else:
            return None

    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade', string='employee', readonly=True,
                                  states={'draft': [('readonly', False)]}, default=_applyUser,)

    # 制表人
    create_user = fields.Many2one('res.users', string='create user', default=lambda self: self._uid, readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 创建时间
    create_date = fields.Datetime(string='create time', default=lambda self: datetime.now(), readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 原岗位
    original_post = fields.Many2one(related='employee_id.workpost', store=True, ondelete='restrict',
                                    string="employees_original_post", readonly=True,
                                    states={'draft': [('readonly', False)]})
    # 原部门
    original_unit = fields.Many2one(related='employee_id.department_id', store=True, ondelete='restrict',
                                    string="employees_original_section", readonly=True,
                                    states={'draft': [('readonly', False)]})

    # 对方单位
    new_unit = fields.Char(string='target unit', readonly=True,
                           states={'draft': [('readonly', False)]})

    # 新岗位
    new_post = fields.Char(string='new post', readonly=True,
                           states={'draft': [('readonly', False)]})

    # 状态
    state = fields.Selection([("draft", "employees_unit_draft"),  # 草稿
                              ("confirmed", "employees_unit_confirmed"),  # 待审批
                              ("done", "employees_unit_done"),  # 已完成
                              ], default='draft', string="employees_unit_status")

    # 调动原因
    transfer_reason = fields.Text(string="employees_transfer_reason", readonly=True,
                                  states={'draft': [('readonly', False)]})
    # 审批/会签人员
    countersign_person = fields.Many2many('hr.employee', string="employees_countersign_person", readonly=True,
                                          states={'draft': [('readonly', False)]})

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr_employees.transfer') or '/'
        return super(ForeignTransfer, self).create(vals)

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        record = {
            'name': self.name,
            'transferdate': self.create_date,
            'employee_id': self.employee_id.id,
            'original_unit': self.original_unit.name,
            'original_post': self.original_post.name,
            'new_section': self.new_unit,
            'new_post': self.new_post,
            'transfer_reason': self.transfer_reason,
            'transfer_type': 'foreign_transfer'
        }
        recins = self.env['employees.transfer.record'].create(record)
        countersign_person = []
        for item in self.countersign_person:
            countersign_person.append((4, item.id,))
        recins.write({'countersign_person': countersign_person})

        self.employee_id.write({'active': False})

        self.state = 'done'

    @api.multi
    def unlink(self):
        for order in self:
            if not order.state == 'draft':
                raise exceptions.UserError(_('only delete in state draft'))
        return super(ForeignTransfer, self).unlink()


class TransferRecord(models.Model):
    """
    调动记录
    """
    _name = 'employees.transfer.record'

    # 调动单编码
    name = fields.Char(string="employees_transfer_code")

    # 调动时间
    transferdate = fields.Datetime()

    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')

    # 原部门
    original_unit = fields.Char(string="employees_original_unit")
    # 原单位岗位
    original_post = fields.Char(string="employees_original_post")

    # 新部门
    new_section = fields.Char(string="employees_new_section")
    # 新单位岗位
    new_post = fields.Char(string="employees_new_post")

    # 调动类型
    transfer_type = fields.Selection([("post_transfer", "employees_post_transfer"),  # 岗位调动
                                      ("unit_transfer", "employees_unit_transfer"),  # 单位调动
                                      ("foreign_transfer", "employees_foreign_transfer"),  # 对外调动
                                      ], string="employees_foreign_transfer_type")

    # 调动原因
    transfer_reason = fields.Text(string="employees_transfer_reason")

    # 审批/会签人员
    countersign_person = fields.Many2many('hr.employee', string="employees_countersign_person")
