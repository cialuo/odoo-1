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


class post(models.Model):
    """
    岗位设置
    """
    _name = 'employees.post'

    # 岗位名称
    name = fields.Char(_('employees post name'))
    # 岗位所在部门
    department = fields.Many2one('hr.department', ondelete='restrict', string= _('post department'), required=True)
    # 岗位信息
    description = fields.Char(string=_('post infomation'))
    # 岗位类型
    posttype = fields.Selection([
        ('manager',_('post title manager')),        #经理
        ('labour',_('post title labour'))           #员工
    ], string=_('post title list'), required=True)
    # 岗位员工
    members = fields.One2many('hr.employee', 'workpost', string=_('post members'))
    # 直接领导
    direct_leader = fields.Char(compute='_getDirectLeader', string=_('deirect leader'))
    @api.onchange('department')
    def _getDirectLeader(self):
        for item in self:
            parentDepartmentId = item.department.parent_id.id
            managerPosts = self.getPostListInDepartment(parentDepartmentId, postType='manager')
            if len(managerPosts) != 0:
                managerList = self.getEmployeesWithSpecifyPost(managerPosts[0].id)
                item.direct_leader = '\\'.join([manager['name'] for manager in managerList ])
            else:
                item.direct_leader = ''

    def getPostListInDepartment(self, departmentId, postType=None):
        """
        获取指定部门下的岗位列表
        :param departmentId 部门ID号
        :param postType 岗位类型
        :return 返回岗位列表
        """
        constrains = [('department','=', departmentId)]
        if postType != None:
            constrains.append(('posttype', '=', postType))
        postList = self.search(constrains)
        return postList

    def getEmployeesWithSpecifyPost(self, postid):
        """
        获取指定岗位下的全部员工信息
        :param postid  岗位ID
        """
        employeeMode = self.env['hr.employee']
        employeeList = employeeMode.search([('workpost', '=', postid)])
        return [{'id':item.id, 'name':item.name} for item in employeeList]
        

    # 上级部门 
    higher_level = fields.Char(compute='_getHigherLevel', string=_('higher level'))
    @api.onchange('department')
    def _getHigherLevel(self):
        for item in self:
            parentDepartments = []
            self.getParentDepartment(item.department.id, parentDepartments)
            parentDepartments = parentDepartments[::-1]
            self.higher_level = '\\'.join(parentDepartments)
    
    def getParentDepartment(self, parentId, container):
        """
        递归获取上级部门名称
        """
        if parentId:
            departmentMode = self.env['hr.department']
            result = departmentMode.search([('id','=', parentId)], limit=1)
            if len(result) > 0:
                record = result[0]
                container.append(record.name)
                if record.parent_id != None:
                    self.getParentDepartment(record.parent_id.id, container)



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


class LtyGroups(models.Model):
    """
    重载系统 群组 设置
    """
    _inherit = "res.groups"

    # 是否可以作为角色
    isrole = fields.Boolean(default=False, string=_('is role'))

    # 关联的岗位
    post_id = fields.Many2one('employees.post', string = _('related post'))

    @api.constrains('post_id')
    def _checkPostNotSetBefore(self):
        """
        当一个岗位已经设置权限后，不能再设置权限
        """
        for item in self:
            postid = item.post_id.id
            count = self.search_count([('post_id', '=', postid)])
            if count > 0:
                raise exceptions.ValidationError(_("can't set post's group in twice"))

