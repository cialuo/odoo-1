# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class employee(models.Model):
    _inherit = 'hr.employee'

    # 工号
    jobnumber = fields.Char(string='employee work number', required=True)
    # 职称
    title = fields.Char(string='emplyee title')
    # 入职时间
    entrydate = fields.Date(string='employee entry date')
    # 转正时间
    passdate = fields.Date(string='emplyee pass time')
    # 员工状态
    employeestate = fields.Selection([
        ('in_work', 'employee state in work'),  # 在职
        ('retired', 'employee state retired'),  # 退休
        ('inner_retired', 'employee state inner retired'),  # 内退
        ('retired_pay', 'employee state retired pay'),  # 退养
        ('injured', 'employee state injured'),  # 工伤
        ('other', 'employee state other'),  # 其他
    ], string='emplyee state')
    # 人员属性
    employeeattr = fields.Char(string='emplyee attribute')
    # 劳动合同
    bargain = fields.Char(string='emplyee bargain')
    # 驾驶证类别
    drivelicense = fields.Char(string='emplyee drivelicense type')
    # 驾驶证号码
    drivelicensenumber = fields.Char(string='emplyee drivelicense number')
    # 驾驶证领证日期
    drivelicensedata = fields.Date(string='emplyee drivelicense date')
    # 社保账户
    socialsecurityaccount = fields.Char(string='employee socialsecurity account')
    # 工资账户
    salaryaccount = fields.Char(string='employee salary account')

    # 员工家属信息
    families = fields.One2many('employees.employeefamily', 'employee_id', string="employees's families")
    # 员工所在岗位
    workpost = fields.Many2one('employees.post', ondelete='restrict', string='employee work post', required=True)

    # 婚姻状况
    marital_status = fields.Selection([
        ('married','married'),              # 已婚
        ('spinsterhood','spinsterhood'),    # 未婚
    ], string='marital status')

    # 生日
    birthday = fields.Date('birth day')
    # 籍贯
    native_place = fields.Char('native place')
    # 专业
    specialty = fields.Char('specialty')
    # 民族
    nation = fields.Char('nation')
    # 身份证号
    id_card = fields.Char('ID Card')
    # 学历
    education = fields.Char('education')
    # 政治面貌
    political_status = fields.Char('political status')
    # 住址
    live_address = fields.Char('live address')
    # 性别
    sex = fields.Selection([
        ('male','male'),                    # 男
        ('female','female')                 # 女
    ], string='sex', required=True)

    # 员工单位调动
    unit_transfer = fields.One2many('employees.unit', 'employee_id', string="employees_unit_transfer")

    @api.constrains('user_id')
    def _relateone2one(self):
        """
        一个系统用户只能绑定到一个员工
        """
        for item in self:
            uid = item.user_id.id
            if uid == 1:
                # 超级管理员不能被绑定到员工
                raise ValidationError(_("administrator can not be bind to an employee"))
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

        if workpost != None and user_id == None:
            # 岗位调整 关联用户未调整
            # 修改关联用户的权限 先删除用户老岗位权限
            # 然后增加用户当前新岗位权限
            if self.workpost != None and self.user_id.id != False:
                # 如果之前指定了岗位 并且 之前也绑定了系统用户
                deleteUserGroup(self, self.user_id.id)
            if self.user_id.id != False:
                # 如果之前绑定了用户
                self._powerRebuild(self.user_id.id, workpost, 'add')
        elif workpost != None and user_id != None:
            # 岗位调整 关联用户也调整
            # 将老用户的权限老岗位的权限解绑
            # 将新用户的权限跟新岗位的权限绑定
            if self.workpost != None and self.user_id.id != False:
                # 如果之前指定了岗位 并且 之前也绑定了系统用户
                deleteUserGroup(self, self.user_id.id)
            self._powerRebuild(user_id, workpost, 'add')
        elif workpost == None and user_id == None:
            # 岗位未调整 关联用户也未调整
            # 无需处理
            pass
        elif workpost == None and user_id != None:
            # 岗位未调整 用户有调整
            # 将老用户的权限跟当前岗位的权限解绑
            # 将新用户的权限跟当前岗位的权限绑定
            if self.user_id.id != False and self.workpost != None:
                # 将老用好的岗位权限解绑
                deleteUserGroup(self, self.user_id.id)
            if self.workpost != None:
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
        if groupinfo.id == False:
            # 如果组没有被绑定到岗位 则无需处理
            return
        groupid = groupinfo.id
        userinfo = usermode.search([('id', '=', userid)], limit=1)
        if userinfo.id == False:
            # 没找到用户信息 不处理
            return
        if operator == 'add':
            # 给用户增加权限
            userinfo.write({'groups_id': [(4, groupid, 0)]})
        elif operator == 'remove':
            # 给用户删除权限
            userinfo.write({'groups_id': [(3, groupid, 0)]})

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


def deleteUserGroup(self, userid):
    """
    删除用户所有的组
    """
    if userid == 1:
        # 超级管理员不执行权限删除
        return
    usersmode = self.env['res.users']
    userinfo = usersmode.search([('id', '=', userid)], limit=1)
    if userinfo.id != False:
        gids = []
        for item in userinfo.groups_id:
            gids.append(item.id)
        delsql = []
        for item in gids:
            delsql.append((3, item, 0))
        userinfo.write({'groups_id': delsql})


class EmployeeFamily(models.Model):
    """
    员工家属信息表
    """
    _name = 'employees.employeefamily'

    # 名称
    name = fields.Char(string='family name')
    # 家庭关系
    relation = fields.Char(string='family relation')
    # 性别
    sex = fields.Selection([
        ('male', 'male'),
        ('female', 'female')
    ], string='sex')
    # 职业
    profession = fields.Char(string='family profession')
    # 电话
    phone = fields.Char(string='family phone')
    # 工作单位
    employer = fields.Char(string='family employer')
    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')


class post(models.Model):
    """
    岗位设置
    """
    _name = 'employees.post'

    # 岗位名称
    name = fields.Char('employees post name')
    # 岗位所在部门
    department = fields.Many2one('hr.department', ondelete='restrict', string='post department', required=True)
    # 岗位信息
    description = fields.Char(string='post infomation')
    # 岗位类型
    posttype = fields.Selection([
        ('manager', 'post title manager'),  # 经理
        ('labour', 'post title labour'),  # 员工
        ('driver', 'post title driver'),  # 司机
        ('conductor', 'post title conductor')  # 售票员
    ], string='post title list', required=True)
    # 岗位员工
    members = fields.One2many('hr.employee', 'workpost', string='post members')
    # 关联群组
    group_id = fields.Char(compute='_getRelateGroup', string='post relate group')

    @api.multi
    def _getRelateGroup(self):
        groupmode = self.env['res.groups']
        for item in self:
            groupinfo = groupmode.search([('post_id', '=', item.id)], limit=1)
            if groupinfo.id != False:
                item.group_id = groupinfo.name
            else:
                item.group_id = ''

    # 直接领导
    direct_leader = fields.Char(compute='_getDirectLeader', string='deirect leader')

    @api.onchange('department')
    def _getDirectLeader(self):
        for item in self:
            parentDepartmentId = item.department.parent_id.id
            managerPosts = self.getPostListInDepartment(parentDepartmentId, postType='manager')
            if len(managerPosts) != 0:
                managerList = self.getEmployeesWithSpecifyPost(managerPosts[0].id)
                item.direct_leader = '\\'.join([manager['name'] for manager in managerList])
            else:
                item.direct_leader = ''

    def getPostListInDepartment(self, departmentId, postType=None):
        """
        获取指定部门下的岗位列表
        :param departmentId 部门ID号
        :param postType 岗位类型
        :return 返回岗位列表
        """
        constrains = [('department', '=', departmentId)]
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
        return [{'id': item.id, 'name': item.name} for item in employeeList]

    # 上级部门
    higher_level = fields.Char(compute='_getHigherLevel', string='higher level')

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
            result = departmentMode.search([('id', '=', parentId)], limit=1)
            if len(result) > 0:
                record = result[0]
                container.append(record.name)
                if record.parent_id != None:
                    self.getParentDepartment(record.parent_id.id, container)

    # 岗位下的员工数量
    membercount = fields.Char(compute='_countpostmember', string='member count of post')

    def _countpostmember(self):
        for item in self:
            employeemode = self.env['hr.employee']
            count = employeemode.search_count([('workpost', '=', item.id)])
            item.membercount = str(count)


class department(models.Model):
    _inherit = 'hr.department'

    # 岗位数量
    membercount = fields.Char(compute='_countmember', string='post count in department')

    @api.multi
    def _countmember(self):
        for item in self:
            postModel = self.env['employees.post']
            item.membercount = str(postModel.search_count([('department', '=', item.id)]))

    # 建档时间
    record_createdate = fields.Date(compute='_getRecordCreateTime',
                                    string='department record create time')

    @api.multi
    def _getRecordCreateTime(self):
        for item in self:
            item.record_createdate = item.create_date

    departmenttype = fields.Selection([
        ('headquarters', 'department type headquarters'),  # 总公司
        ('branch', 'department type branch'),  # 分公司
        ('subsidiary', 'department type subsidiary'),  # 子公司
        ('department', 'department type department'),  # 部门
        ('group', 'department type group'),  # 组
    ], string='department type')

    # 部门岗位列表
    post_id = fields.One2many('employees.post', 'department', string='department post list')
    # 岗位成员
    member_id = fields.One2many('hr.employee', 'department_id', string='department employees')


class LtyGroups(models.Model):
    """
    重载系统 群组 设置
    """
    _inherit = "res.groups"

    # 是否可以作为角色
    isrole = fields.Boolean(default=False, string='is role')

    # 关联的岗位
    post_id = fields.Many2one('employees.post', string='related post')

    implied_ids_r = fields.Many2many('res.groups', 'res_groups_implied_rel', 'hid', 'gid',
                                     string='Inherits reversal',
                                     help='Users of this group automatically inherit those groups')

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
        for item in self:
            if isrole_new != item.isrole and isrole_new == False and isrole_new != None:
                # 取消群组的角色勾选框
                if item.post_id.id != False:
                    # 如果之前指定了岗位 则将岗位下所有的人的权限去掉 同时将postid置空
                    self.updateUserGroup(None if item.post_id.id == False else item.post_id.id, None, item.id)
                    vals['post_id'] = None

            if isrole_new != item.isrole and isrole_new == True and isrole_new != None:
                # 将角色勾选框选中
                if post_id_new != None:
                    # 如果指定了岗位id 则更新岗位下的用户权限
                    self.updateUserGroup(None if item.post_id.id == False else item.post_id.id, post_id_new, item.id)
            if post_id_new != self.post_id.id and self.isrole == True and post_id_new != None:
                # 如果角色勾选框没有修改 并且 岗位id值出现变化 并且 isrole值原本就是true
                # 则修改对应的岗位员工的权限值
                self.updateUserGroup(None if item.post_id.id == False else item.post_id.id, post_id_new, item.id)

        res = super(LtyGroups, self).write(vals)

        for item in self:
            if vals.get('implied_ids'):
                # 修改了继承关系 要重建所有的继承了该group的岗位权限
                gid = item.id
                inheritors = set()
                self._getGroupinheritor(gid, inheritors)
                inheritors.add(gid)
                for groupid in inheritors:
                    self._rebuildGroupUser(groupid)

        return res

    def updateUserGroup(self, old, new, groupid):
        """
        更新用户组权限
        @param  old 之前的岗位id
        @param new 新的岗位id
        @param groupid 当前的goupid
        """
        usermode = self.env['hr.employee']
        if old != None:
            # 删除之前岗位下用户的权限
            users = usermode.search([('workpost', '=', old)])
            for item in users:
                if item.user_id.id != False:
                    deleteUserGroup(usermode, item.user_id.id)

        if new != None:
            # 给新岗位下的用户添加权限
            users = usermode.search([('workpost', '=', new)])
            for item in users:
                if item.user_id.id != False:
                    item.user_id.write({'groups_id': [(4, groupid, 0)]})

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
            if item.isrole or item.post_id.id != False:
                # 如果一个群组是一个角色 或者 已经绑定到岗位 那么该group不能被删除
                raise ValidationError(_('a group that bind with a post can not be delete'))
            inheritors = set()
            self._getGroupinheritor(item.id, inheritors)
            if len(inheritors) > 0:
                # 如果该组被其他组继承 那么该组不能被删除
                raise ValidationError(_('groups are inherited by other groups, can not be delete!'))
            self.updateUserGroup(None if item.post_id.id else item.post_id.id, None, item.id)
        return super(LtyGroups, self).unlink()

    def _getGroupinheritor(self, gid, resultcontainer):
        """
        递归获取继承了该group的群组
        @param gid  群组id
        @param resultcontainer set类型 将查找的id放到该集合里
        """
        groupinfo = self.search([('id', '=', gid)], limit=1)
        if groupinfo.id == False:
            return
        inheritors = groupinfo.implied_ids_r
        for item in inheritors:
            if item.id not in resultcontainer:
                # 如果之前没有遍历到才继续递归 **防止循环继承导致无限递归**
                resultcontainer.add(item.id)
                self._getGroupinheritor(item.id, resultcontainer)

    def _rebuildGroupUser(self, groupid):
        groupinfo = self.search([('id', '=', groupid)], limit=1)
        if groupinfo.id == False:
            # 没找到岗位信息 不处理
            return
        if groupinfo.isrole == None or groupinfo.post_id.id == False:
            # 如果该组不是角色 或者 没有绑定到岗位 不处理
            return
        employeemode = self.env['hr.employee']
        postid = groupinfo.post_id.id
        employeelist = employeemode.search([('workpost', '=', postid)])
        for item in employeelist:
            if item.user_id.id != False:
                # 先删除用户的组 然后在重新添加用户的组
                deleteUserGroup(self, item.user_id.id)
                item.user_id.write({'groups_id': [(4, groupid, 0)]})


class UnitTransfer(models.Model):
    """
     单位调动
    """
    _name = 'employees.unit'

    # 调动单编码
    name = fields.Char(string="employees_transfer_code", help='employees_transfer_code', required=True, index=True,
                       copy=False, default='New', readonly=True)
    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')
    # # 录入时间
    # entering_date = fields.Date(string="employees_entering_date")
    # # 录单人
    # record_person = fields.Char(string="employees_record_person")
    # 原单位
    original_unit = fields.Many2one('hr.department', related="employee_id.department_id",
                                    string="employees_original_unit", store=False)
    # 原单位岗位
    original_post = fields.Many2one('employees.post', ondelete='restrict', related="employee_id.workpost",
                                    string="employees_original_post", store=False)
    # 原部门
    original_section = fields.Many2one('hr.department', related="employee_id.department_id",
                                       string="employees_original_section", store=False)
    # 原工资结构
    original_wage = fields.Char(string="employees_original_wage")
    # 新单位
    new_unit = fields.Many2one('hr.department', related="employee_id.department_id",
                               string="employees_new_unit", store=False)
    # 新单位岗位
    new_post = fields.Many2one('employees.post', ondelete='restrict', related="employee_id.workpost",
                               string="employees_new_post", store=False)
    # 新部门
    new_section = fields.Many2one('hr.department', related="employee_id.department_id",
                                  string="employees_new_section", store=False)
    # 新工资结构
    new_wage = fields.Char(string="employees_new_wage")
    # 状态
    state = fields.Selection([("draft", "employees_unit_draft"),  # 草稿
                              ("confirmed", "employees_unit_confirmed"),  # 待审批
                              ("done", "employees_unit_done"),  # 已完成
                              ], default='draft', string="employees_unit_status")

    # 调动原因
    transfer_reason = fields.Text(string="employees_transfer_reason")
    # 审批/会签人员
    countersign_person = fields.Many2many('hr.employee', string="employees_countersign_person")

    @api.model
    def create(self, vals):
        """
        单位调动:
            自动生成订单号：前缀NBDD+序号
        """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr_employees.transfer') or '/'
        return super(UnitTransfer, self).create(vals)

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'


class PostTransfer(models.Model):
    """
    岗位调动
    """
    _name = 'employees.post.transfer'

    # 调动单编码
    name = fields.Char(string="employees_transfer_code", help='employees_transfer_code', required=True, index=True,
                       copy=False, default='New', readonly=True)
    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')
    # 录入时间
    # entering_date = fields.Date(string="employees_entering_date")
    # # 录单人
    # record_person = fields.Char(string="employees_record_person")
    # 单位
    original_unit = fields.Many2one('hr.department', related="employee_id.department_id",
                                    string="employees_post_unit")
    # 原单位岗位
    original_post = fields.Many2one('employees.post', ondelete='restrict', related="employee_id.workpost",
                                    string="employees_original_post")
    # 新单位岗位
    new_post = fields.Many2one('employees.post', ondelete='restrict', related="employee_id.workpost",
                               string="employees_new_post")

    # 部门
    post_section = fields.Many2one('hr.department', related="employee_id.department_id",
                                   string="employees_post_section")
    # 原工资结构
    original_wage = fields.Char(string="employees_original_wage")
    # 新工资结构
    new_wage = fields.Char(string="employees_new_wage")

    # 状态
    state = fields.Selection([("draft", "employees_unit_draft"),  # 草稿
                              ("confirmed", "employees_unit_confirmed"),  # 待审批
                              ("done", "employees_unit_done"),  # 已完成
                              ], default='draft', string="employees_unit_status")

    # 调动原因
    transfer_reason = fields.Text(string="employees_transfer_reason")
    # 审批/会签人员
    countersign_person = fields.Many2many('hr.employee', string="employees_countersign_person")

    @api.model
    def create(self, vals):
        """
        单位调动:
            自动生成订单号：前缀NBDD+序号
        """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr_employees.transfer') or '/'
        return super(PostTransfer, self).create(vals)

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'


class ForeignTransfer(models.Model):
    """
    对外调动
    """
    _name = 'employees.foreign'

    # 调动单编码
    name = fields.Char(string="employees_transfer_code", help='employees_transfer_code', required=True, index=True,
                       copy=False, default='New', readonly=True)
    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')
    # # 录入时间
    # entering_date = fields.Date(string="employees_entering_date")
    # # 录单人
    # record_person = fields.Char(string="employees_record_person")
    # 单位
    original_unit = fields.Many2one('hr.department', related="employee_id.department_id",
                                    string="employees_post_unit")
    # 原单位岗位
    original_post = fields.Many2one('employees.post', ondelete='restrict', related="employee_id.workpost",
                                    string="employees_original_post")
    # 对方单位
    new_unit = fields.Many2one('hr.department', related="employee_id.department_id",
                               string="employees_foreign_new_unit")
    # 调动类型
    transfer_type = fields.Selection([("transfer_out", "transfer_out"),  # 迁出
                                      ("transfer_in", "transfer_in"),  # 迁入
                                      ], string="employees_foreign_transfer_type")
    # 部门
    foreign_section = fields.Many2one('hr.department', related="employee_id.department_id",
                                      string="employees_foreign_section")
    # 工资结构
    wage = fields.Char(string="employees_foreign_wage")
    # 状态
    state = fields.Selection([("draft", "employees_unit_draft"),  # 草稿
                              ("confirmed", "employees_unit_confirmed"),  # 待审批
                              ("done", "employees_unit_done"),  # 已完成
                              ], default='draft', string="employees_unit_status")

    # 调动原因
    transfer_reason = fields.Text(string="employees_transfer_reason")
    # 审批/会签人员
    countersign_person = fields.Many2many('hr.employee', string="employees_countersign_person")

    @api.model
    def create(self, vals):
        """
        单位调动:
            自动生成订单号：前缀NBDD+序号
        """
        if vals.get('name', 'New') == 'New':
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
        self.state = 'done'


class TransferRecord(models.Model):
    """
    调动记录
    """
    _name = 'employees.transfer.record'
    _description = ''

    # 调动单编码
    name = fields.Char(string="employees_transfer_code")
    # 关联的员工
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')
    # 调动时间
    # entering_date = fields.Date(string="employees_transfer_date")
    # # 调动人
    # record_person = fields.Char(string="employees_transfer_person")
    # 原单位
    original_unit = fields.Many2one('hr.department', related="employee_id.department_id",
                                    string="employees_original_unit")
    # 原单位岗位
    original_post = fields.Many2one('employees.post', ondelete='restrict', related="employee_id.workpost",
                                    string="employees_original_post")
    # 原部门
    original_section = fields.Many2one('hr.department', related="employee_id.department_id",
                                       string="employees_original_section")
    # 原工资结构
    original_wage = fields.Char(string="employees_original_wage")
    # 新单位
    new_unit = fields.Many2one('hr.department', related="employee_id.department_id",
                                string="employees_new_unit")
    # 新单位岗位
    new_post = fields.Many2one('employees.post', ondelete='restrict', related="employee_id.workpost",
                               string="employees_new_post")
    # 新部门
    new_section = fields.Many2one('hr.department', related="employee_id.department_id",
                                  string="employees_new_section")
    # 新工资结构
    new_wage = fields.Char(string="employees_new_wage")
    # 调动类型
    transfer_type = fields.Selection([("post_transfer", "employees_post_transfer"),  # 岗位调动
                                      ("unit_transfer", "employees_unit_transfer"),  # 单位调动
                                      ("foreign_transfer", "employees_foreign_transfer"),  # 对外调动
                                      ], string="employees_foreign_transfer_type")

    # 调动原因
    transfer_reason = fields.Text(string="employees_transfer_reason")
    # 审批/会签人员
    countersign_person = fields.Many2many('hr.employee', string="employees_countersign_person")
