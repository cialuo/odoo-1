# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class employee(models.Model):
    _inherit = 'hr.employee'

    # 工号
    jobnumber = fields.Char(string=_('employee work number'))
    # 工作单位
    employer = fields.Char(string=_('employee employer'))
    # 职称
    title = fields.Char(string=_('emplyee title'))
    # 入职时间
    entrydate = fields.Date(string=_('employee entry date'))
    # 转正时间
    passdate = fields.Date(string=_('emplyee pass time'))
    # 员工状态
    employeestate = fields.Selection([
        ('in_work', _('employee state in work')),  # 在职
        ('retired', _('employee state retired')),  # 退休
        ('inner_retired', _('employee state inner retired')),  # 内退
        ('retired_pay', _('employee state retired pay')),  # 退养
        ('injured', _('employee state injured')),  # 工伤
        ('other', _('employee state other')),  # 其他
    ], string=_('emplyee state'))
    # 人员属性
    employeeattr = fields.Char(string=_('emplyee attribute'))
    # 劳动合同
    bargain = fields.Char(string=_('emplyee bargain'))
    # 驾驶证类别
    drivelicense = fields.Char(string=_('emplyee drivelicense type'))
    # 驾驶证号码
    drivelicensenumber = fields.Char(string=_('emplyee drivelicense number'))
    # 驾驶证领证日期
    drivelicensedata = fields.Date(string=_('emplyee drivelicense date'))
    # 社保账户
    socialsecurityaccount = fields.Char(string=_('employee socialsecurity account'))
    # 工资账户
    salaryaccount = fields.Char(string=_('employee salary account'))


    # 员工家属信息
    families = fields.One2many('employees.employeefamily', 'employee_id', string=_("employees's families"))
    # 员工所在岗位
    workpost = fields.Many2one('employees.post', ondelete='set null',  string=_('employee work post'))


class EmployeeFamily(models.Model):
    """
    员工家属信息表
    """
    _name = 'employees.employeefamily'

    # 名称
    name = fields.Char(string=_('family name'))
    # 家庭关系
    relation = fields.Char(string=_('family relation'))
    # 性别
    sex = fields.Selection([
        ('male', _('male')),
        ('female', _('female'))
    ],string=_('sex'))
    # 职业
    profession = fields.Char(string=_('family profession'))
    # 电话
    phone = fields.Char(string=_('family phone'))
    # 工作单位
    employer = fields.Char(string=_('family employer'))
    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')

class WorkInfo(models.Model):
    """
    工作信息
    """

    _name = 'employees.workinfo'

    # 工号
    jobnumber = fields.Char(string=_('employee work number'))
    # 工作单位
    employer = fields.Char(string=_('employee employer'))
    # 职称
    title  = fields.Char(string=_('emplyee title'))
    # 入职时间
    entrydate = fields.Date(string=_('employee entry date'))
    # 转正时间
    passdate = fields.Date(string=_('emplyee pass time'))
    # 员工状态
    employeestate = fields.Selection([
        ('in_work', _('employee state in work')),               #在职
        ('retired', _('employee state retired')),               #退休
        ('inner_retired', _('employee state inner retired')),   #内退
        ('retired_pay', _('employee state retired pay')),       #退养
        ('injured', _('employee state injured')),               #工伤
        ('other', _('employee state other')),                   #其他
    ], string=_('emplyee state'))
    # 人员属性
    employeeattr = fields.Char(string=_('emplyee attribute'))
    # 劳动合同
    bargain = fields.Char(string=_('emplyee bargain'))
    # 驾驶证类别
    drivelicense = fields.Char(string=_('emplyee drivelicense type'))
    # 驾驶证号码
    drivelicensenumber = fields.Char(string=_('emplyee drivelicense number'))
    # 驾驶证领证日期
    drivelicensedata = fields.Date(string=_('emplyee drivelicense date'))



class post(models.Model):
    """
    岗位设置
    """
    _name = 'employees.post'

    # 岗位所在部门
    department = fields.Many2one('hr.department', ondelete='restrict', string= _('post department'))
    # 岗位信息
    description = fields.Char(string=_('post infomation'))
    # 岗位类型
    posttype = fields.Selection([
        ('manager',_('post title manager')),        #经理
        ('labour',_('post title labour'))           #员工
    ], string=_('post title list'))
    # 岗位员工
    menbers = fields.One2many('hr.employee', 'workpost', string=_('post members'))

class department(models.Model):

    _inherit = 'hr.department'

    # 成员数量
    membercount = fields.Char(compute='_countmember', string=_('member count in department'))

    @api.multi
    def _countmember(self):
        for item in self:
            employeeModel = self.env['hr.employee']
            item.membercount = str(employeeModel.search_count([('department_id', '=', item.id)]))

    # 建档时间
    record_createdate = fields.Date(compute='_getRecordCreateTime',
                                    string=_('department record create time'))
    @api.multi
    def _getRecordCreateTime(self):
        for item in self:
            item.record_createdate = item.create_date

    departmenttype = fields.Selection([
        ('headquarters', _('department type headquarters')),
        ('branch', _('department type branch')),
        ('subsidiary', _('department type subsidiary')),
        ('department', _('department type department')),
        ('group', _('department type group')),
    ], _('department type'))



    # 部门岗位列表
    post_id = fields.One2many('employees.post', 'department', string=_('department post list'))
    # 岗位成员
    member_id = fields.One2many('hr.employee', 'department_id', string=_('department employees'))
