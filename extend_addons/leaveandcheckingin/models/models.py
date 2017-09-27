# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError
import odoo.tools.misc
import time
# 休假与考勤

class attence(models.Model):
    """
    考勤记录
    """
    _name = 'employee.attencerecords'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='employee')


    # 上班打卡时间
    checkingin = fields.Datetime(string='checkingin time')

    # 下班打卡时间
    checkinginout = fields.Datetime(string='checkingout time')

    # 缺勤时长
    length = fields.Integer(string="time length")

    # 状态
    status = fields.Selection([
        ('late', 'late'),
        ('early', 'early'),
        ('late+early', 'late+early')
    ], string='status')


class attencededucted(models.Model):
    """
    考勤扣款
    """
    _name = 'employee.attencededucted'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='employee', required=True)

    # 内部编号
    jobnumber = fields.Char(related='employee_id.jobnumber')

    # 考勤月份
    month = fields.Date(string='attence month', required=True)

    # 缺勤时长 分钟单位
    absence = fields.Integer(string='attence absence', required=True)

    # 扣款金额
    deducted = fields.Integer(string='deducted money', required=True)

    @api.one
    @api.constrains('absence', 'deducted')
    def _check_description(self):
        if self.absence < 0:
            raise ValidationError(_("absence time must be an positive integer"))

        if self.deducted < 0:
            raise ValidationError(_("deducted must be an positive integer"))

    @api.model
    def _formatTime(self, month):
        return time.strftime("%Y-%m-01",
                      time.localtime(time.mktime(time.strptime(month, "%Y-%m-%d"))))

    @api.model
    def _isDuplicate(self, employee, month):
        return self.search_count([('month' , '=', month), ('employee_id', '=', employee)])

    @api.multi
    def write(self, vals):
        month = vals.get('month', None)
        if month != None:
            month = self._formatTime(month)
            vals['month'] = month
        for item in self:
            if self._isDuplicate(item.employee_id.id, month) >= 1:
                raise ValidationError(_("record duplicated"))
        return super(attencededucted,self).write(vals)

    def getEmployeeInfo(self, usercode):
        employeemode = self.env['hr.employee']
        vechileinfo = employeemode.search([('jobnumber', '=', usercode)], limit=1)
        if len(vechileinfo) == 0:
            return False
        else:
            return vechileinfo[0]

    @api.model
    def create(self, vals):
        if vals.get('jobnumber', None) != None:
            employeeinfo = self.getEmployeeInfo(vals['jobnumber'])
            if employeeinfo == False:
                raise ValidationError(_("jobnumber notexist"))
            vals['employee_id'] = employeeinfo.id

        vals['month'] = self._formatTime(vals['month'])
        if self._isDuplicate(vals['employee_id'], vals['month']) >= 1:
            raise ValidationError(_("record duplicated"))
        return super(attencededucted,self).create(vals)

    def buidMessage(self, type='error', message='', moreinfo='', to=-1, frm=-1):
        return dict(
            {'record': 0, 'rows': {'to': to, 'from': frm}},
            type=type, message=message,
            moreinfo=moreinfo
        )

    @api.model
    def load(self, fields, data):
        returnVal = {'ids': False, 'messages': []}
        if 'month' not in fields:
            returnVal['messages'].append(
                self.buidMessage(message=_('need date'),
                                 moreinfo=_('must have date in data file'))
            )
            return returnVal
        elif 'absence' not in fields:
            returnVal['messages'].append(
                self.buidMessage(message=_('need absence length'),
                                 moreinfo=_('must have absence length in data file'))
            )
            return returnVal
        elif 'deducted' not in fields:
            returnVal['messages'].append(
                self.buidMessage(message=_('need deducted'),
                                 moreinfo=_('must have deducted in data file'))
            )
            return returnVal
        elif 'jobnumber' not in fields:
            returnVal['messages'].append(
                self.buidMessage(message=_('need jobnumber'),
                                 moreinfo=_('must have jobnumber in data file'))
            )
            return returnVal

        for index, item in enumerate(data):
            item = dict(zip(fields, item))
            try:
                item['deducted'] = int(item['deducted'])
            except exceptions:
                returnVal['messages'].append(
                    self.buidMessage(message=_('deducted must be an integer'),
                                     moreinfo='',frm=index, to=index)
                )
                return returnVal

            try:
                item['absence'] = int(item['absence'])
            except exceptions:
                returnVal['messages'].append(
                    self.buidMessage(message=_('absence must be an integer'),
                                     moreinfo='',frm=index, to=index)
                )
                return returnVal

            if item['deducted'] < 0:
                returnVal['messages'].append(
                    self.buidMessage(message=_('deducted must not negative'),
                                     moreinfo='',frm=index, to=index)
                )
                return returnVal

            if item['absence'] < 0:
                returnVal['messages'].append(
                    self.buidMessage(message=_('absence must not negative'),
                                     moreinfo='',frm=index, to=index)
                )
                return returnVal

            employeeinfo = self.getEmployeeInfo(item['jobnumber'])
            if employeeinfo == False:
                returnVal['messages'].append(
                    self.buidMessage(message=_('jobnumber notexist'),
                                     moreinfo='',frm=index, to=index)
                )
                return returnVal
            month = self._formatTime(item['month'])
            if self._isDuplicate(employeeinfo.id, month) >= 1:
                returnVal['messages'].append(
                    self.buidMessage(message=_('record duplicated') ,
                                     moreinfo='',frm=index, to=index)
                )
                return returnVal
        res = super(attencededucted, self).load(fields, data)
        return res


class LeaveType(models.Model):
    """
    请假类型
    """
    _inherit = 'hr.holidays.status'
    _rec_name = 'namestr'

    _sql_constraints = [('leave type unique', 'unique (name)', 'leave type code Can not duplication')]

    # 类型名称
    namestr = fields.Char(string='type name')

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.namestr
            res.append((record.id, name))
        return res


class LeaveConfig(models.Model):
    _name = 'leave.config.settings'

    # 加班转调休过期天数
    expiretime = fields.Integer(string='overtime expire time')


    @api.multi
    def action_save(self):
        pass


class WorkOvertime(models.Model):
    """
    加班申请
    """
    _name = 'leave.workovertime'
    _rec_name = 'employee_id'

    def init(self):
        cr = self._cr
        cr.execute("""SELECT indexname FROM pg_indexes WHERE indexname = 'leave_workovertime_statusfilter_idx'""")
        if not cr.fetchone():
            cr.execute("""CREATE INDEX leave_workovertime_statusfilter_idx
                          ON leave_workovertime
                          (type, useup, expiretime)""")

    def _applyUser(self):
        userid = self._uid
        users = self.env['hr.employee'].search([('user_id', '=', userid)])
        if len(users) != 0:
            return users[0].id
        else:
            return None

    employee_id = fields.Many2one('hr.employee', string='employee', default=_applyUser, required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 开始时间
    start = fields.Datetime(string='start time', required=True, readonly=True,
                            states={'draft': [('readonly', False)]})

    # 结束时间
    end = fields.Datetime(string='end time', required=True, readonly=True,
                          states={'draft': [('readonly', False)]})

    # 状态
    state = fields.Selection([
        ('draft', 'draft'),  # 草稿
        ('submitted', 'submitted'),  # 已提交
        ('confirmed', 'confirmed')  #
    ], string="status", default='draft')

    # 加班类型
    type = fields.Selection([
        ('default', 'default'),  # 默认
        ('money', 'money'),  # 加班费
        ('offset', 'offset'),  # 调休
    ], string='overtime type', required=True, default='default', readonly=True,
        states={'draft': [('readonly', False)]})

    # 制表人
    create_user = fields.Many2one('res.users', string='create user', default=lambda self: self._uid)

    # 审批/会签人员
    countersign_person = fields.Many2one('res.users', string="employees_countersign_person")

    # 加班时长 小时单位
    length = fields.Integer(string='work overtime length(hour)', required=True, readonly=True,
                            states={'draft': [('readonly', False)]})

    # 剩余可扣除假期
    residue = fields.Integer(string='residue time')

    # 若调休用完 则置为False
    useup = fields.Boolean(string='time use up', default=False)

    # 转调休过期时间
    expiretime = fields.Datetime(string='expire time')

    @api.multi
    def unlink(self):
        for order in self:
            if not order.state == 'draft':
                raise exceptions.UserError(_('only delete in state draft'))
        return super(WorkOvertime, self).unlink()

    @api.one
    @api.constrains('start', 'end', 'length')
    def _check_description(self):
        if self.start > self.end:
            raise ValidationError(_("start time must earlier then end time"))
        if self.length <= 0:
            raise ValidationError(_("worker overtime must more then one hour"))

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_submitted(self):
        self.state = 'submitted'

    def _calculateExpireTime(self):
        confid = self.env.ref('leaveandcheckingin.leave_default_settings')
        configurs = self.env['leave.config.settings'].browse([confid])
        if len(configurs) > 0:
            x = configurs.ids[0]
            return x.expiretime
        else:
            return -1

    @api.multi
    def action_confirmed(self):
        for item in self:
            expiretime = item._calculateExpireTime()
            if self.type == 'offset':
                self.useup = True
                if expiretime < 0:
                    self.expiretime = date.today()+timedelta(days=365*1000)
                else:
                    self.expiretime = date.today() + timedelta(days=expiretime)
            item.residue = self.length
            item.countersign_person = self._uid
            item.state = 'confirmed'

class offsetDays(models.Model):
    """
    可调休天数
    """
    _inherit = 'hr.employee'

    @staticmethod
    def getOffsetHours(modelObj, employee_id):
        timestr = (datetime.now()-timedelta(hours=8)).strftime(odoo.tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
        workovertime = modelObj.env['leave.workovertime'].search([
            ('type', '=', 'offset'),
            ('useup', '=', True),
            ('expiretime', '>', timestr),
            ('employee_id', '=', employee_id)
        ])
        total = 0
        for item2 in workovertime:
            total += item2.residue
        return total

    @api.multi
    def _offsetHours(self):
        for item in self:
            total = self.getOffsetHours(item, item.id)
            item.offsetHours = total

    # 可调休小时数
    offsetHours = fields.Integer(compute='_offsetHours',string='offset hours(hour)')


class Holidays(models.Model):

    _inherit = 'hr.holidays'

    # 请假时长 小时单位
    length = fields.Integer(string='leave length')

    @api.one
    @api.constrains('length')
    def _check_description(self):
        if self.length <= 0:
            raise ValidationError(_("leave time must more then one hour"))

        # 如果选择的是调休 则需要验证调休时间是否够用
        if self.holiday_status_id.name == 'TX':
            offsetHours = offsetDays.getOffsetHours(self, self.employee_id.id)
            if self.length > offsetHours:
                raise ValidationError(_("No more offset "))

    @api.multi
    def action_approve(self):
        timestr = (datetime.now() - timedelta(hours=8)).strftime(odoo.tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
        workovertime = self.env['leave.workovertime'].search([
            ('type', '=', 'offset'),
            ('useup', '=', True),
            ('expiretime', '>', timestr),
            ('employee_id', '=', self.employee_id.id)
        ])

        length = self.length
        for item in workovertime:
            length = length-item.residue
            if length < 0:
                item.residue = abs(length)
                break
            else:
                item.residue = 0
                item.useup = False

        return super(Holidays, self).action_approve()

    @api.multi
    def name_get(self):
        res = []
        for leave in self:
            res.append((leave.id, _("leave request form")))
        return res
