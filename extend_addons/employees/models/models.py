# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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

    @api.constrains('user_id')
    def _relateone2one(self):
        """
        一个系统用户只能绑定到一个员工
        """
        for item in self:
            uid = item.user_id.id
            if uid != False:
                count = self.search_count([('user_id', '=', uid)])
                if count > 1:
                    raise ValidationError(_("can't set system user to employee in twice"))

    @api.multi
    def write(self, vals):
        #  重载write方法
        workpost = vals.get('workpost', None)
        user_id = vals.get('user_id', None)
        if user_id != None:
            count = self.search_count([('user_id', '=', user_id)])
            if count > 1:
                raise ValidationError(_("can't set system user to employee in twice"))

        if workpost != None and user_id == None :
            # 岗位调整 关联用户未调整
            # 修改关联用户的权限 先删除用户老岗位权限
            # 然后增加用户当前新岗位权限
            if self.workpost != None and self.user_id != None:
                # 如果之前指定了岗位 并且 之前也绑定了系统用户
                self._powerRebuild(self.user_id.id, self.workpost.id, 'remove')
            if self.user_id != None:
                # 如果之前绑定了用户
                self._powerRebuild(self.user_id.id, workpost, 'add')
        elif workpost != None and user_id != None:
            # 岗位调整 关联用户也调整
            # 将老用户的权限老岗位的权限解绑 
            # 将新用户的权限跟新岗位的权限绑定
            if self.workpost != None and self.user_id != None:
                # 如果之前指定了岗位 并且 之前也绑定了系统用户
                self._powerRebuild(self.user_id.id, self.workpost.id, 'remove')
            self._powerRebuild(user_id, workpost, 'add')
        elif workpost == None and user_id == None:
            # 岗位未调整 关联用户也未调整
            # 无需处理
            pass
        elif workpost == None and user_id != None:
            # 岗位未调整 用户有调整
            # 将老用户的权限跟当前岗位的权限解绑
            # 将新用户的权限跟当前岗位的权限绑定
            if self.user_id != None and self.workpost != None:
                # 将老用好的岗位权限解绑
                self._powerRebuild(self.user_id.id, self.workpost.id, 'remove')
            if self.workpost != None :
                # 将新用户的权限绑定
                self._powerRebuild(user_id, self.workpost.id, 'add')
        return super(employee, self).write(vals)

    def _powerRebuild(self, userid, postid, operator):
        """
        更新用户对应岗位的权限
        @param userid 用户id
        @param postid 岗位id
        @param operator 操作类型 add 增加权限 remove 删除权限
        """
        groupmode = self.env['res.groups']
        usermode = self.env['res.users']
        groupinfo = groupmode.search([('post_id', '=', postid)], limit=1)
        if groupinfo == None:
            # 如果组没有被绑定到岗位 则无需处理
            return 
        groupid  = groupinfo.id
        userinfo = usermode.search([('id', '=', userid)], limit=1)
        if userinfo == None:
            # 没找到用户信息 不处理
            return
        if operator == 'add':
            # 给用户增加权限
            userinfo.write({'groups_id':[(4, groupid, 0)]})
        elif operator == 'remove':
            # 给用户删除权限
            userinfo.write({'groups_id':[(3, groupid, 0)]})

    @api.model
    def create(self, vals):
        # 重载create方法
        workpost = vals.get('workpost', False)
        user_id = vals.get('user_id', False)
        if user_id != False:
            count = self.search_count([('user_id', '=', user_id)])
            if count > 1:
                raise ValidationError(_("can't set system user to employee in twice"))
        if workpost != False and user_id != False:
            self._powerRebuild(user_id, workpost, 'add')
        return super(employee, self).create(vals)


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
            if postid != False:
                count = self.search_count([('post_id', '=', postid)])
                if count > 1:
                    raise ValidationError(_("can't set post's group in twice"))

    @api.multi
    def write(self, vals):
        """
        重载write方法
        """
        isrole_new = vals.get('isrole', None)
        post_id_new = vals.get('post_id', None)
        if isrole_new != self.isrole and isrole_new == False and isrole_new != None:
            #取消群组的角色勾选框
            if self.post_id != None:
                #如果之前指定了岗位 则将岗位下所有的人的权限去掉 同时将postid置空
                vals['post_id'] = None
                self.updateUserGroup(None if self.post_id.id == False else self.post_id.id, None, self.id)

        if isrole_new != self.isrole and isrole_new == True and isrole_new != None:
            #将角色勾选框选中
            if post_id_new != None:
                #如果指定了岗位id 则更新岗位下的用户权限
                self.updateUserGroup(None if self.post_id.id == False else self.post_id.id, post_id_new, self.id)
        if post_id_new != self.post_id and self.isrole == True and post_id_new != None:
            # 如果角色勾选框没有修改 并且 岗位id值出现变化 并且 isrole值原本就是true
            # 则修改对应的岗位员工的权限值
            self.updateUserGroup(None if self.post_id.id == False else self.post_id.id, post_id_new, self.id)

        return super(LtyGroups, self).write(vals)

    def updateUserGroup(self, old, new, groupid):
        """
        更新用户组权限
        @param  old 之前的岗位id
        @param new 新的岗位id
        @param groupid 当前的goupid
        """
        usermode = self.env['hr.employee']
        resusermode = self.env['res.users']
        if old != None:
            # 删除之前岗位下用户的权限
            users = usermode.search([('workpost', '=', old)])
            for item in users:
                if item.user_id != None:
                    item.user_id.write({'groups_id':[(3, groupid, 0)]})

        if new != None:
            # 给新岗位下的用户添加权限
            users = usermode.search([('workpost', '=', new)])
            for item in users:
                if item.user_id != None:
                    item.user_id.write({'groups_id':[(4, groupid, 0)]})

    @api.model
    def create(self, vals):
        """
        重载创建方法
        """
        isrole = vals.get('isrole', None)
        postid = vals.get('post_id', None)
        if (isrole == False and postid != None) or (isrole == None and postid != None):
            # 如果没有指定为角色 则将选择的岗位id置为空
            vals['post_id'] = None
        record = super(LtyGroups, self).create(vals)
        if isrole == True and postid != False and postid != None:
            self.updateUserGroup(None, postid, record.id)
        return record

    @api.multi
    def unlink(self):
        # 重载删除方法 
        for item in self:
            self.updateUserGroup(None if item.post_id.id else item.post_id.id, None, item.id)
        return super(LtyGroups, self).unlink()
