# -*- coding: utf-8 -*-

from odoo import models, fields, api,_,exceptions
import datetime
class security_check(models.Model):

    _name = 'energy.security_check'
    _inherit = ['mail.thread']
    _description = 'Security check'
    _sql_constraints = [('security_check_name_unique', 'unique (name)', '检查编号已经存在!')]

    """
       安全检查
    """

    def _default_utcnow(self):
        """
            获取当前UTC时间
        :return:
        """
        return datetime.datetime.utcnow()

    security_check_detail_ids = fields.One2many('energy.security_check_details','security_check_id',string='Security Check Detail Ids')

    name = fields.Char(string='Check No',required=True)

    # 能源站
    station_id = fields.Many2one('energy.station', string='Station Id',required=True,domain=[('station_property','=','company')])

    # 能源站类别
    station_type = fields.Selection(string='Station Type', related='station_id.station_type', store=False,readonly=True)

    # 隶属部门
    department_id = fields.Many2one('hr.department',related='station_id.department_id', store=False,string='Department Id')

    # 巡检人
    patrol_man = fields.Many2one('hr.employee', string='Patrol Man')

    # 责任人
    person_liable = fields.Many2one('hr.employee', string='Person liable',required=True)

    # 巡检日期
    check_date = fields.Datetime(string='Check Date',default=_default_utcnow)

    # 检查结果
    check_result = fields.Char(string='Check Result')

    # 安全检查状态
    state = fields.Selection([('draft','Draft'),('refer','Refer'),('auditing','Auditing'),('complete','Complete')],default='draft',string='Check Result')

    # 巡检类型
    check_type = fields.Selection([('normalinspection','Normal inspection'),('sampling','Sampling')],string='Check Type',required=True,default='normalinspection')

    # 备注
    remarks = fields.Char('Remarks')


    @api.onchange('station_id')
    def _onchange_station_id(self):
        """
            在能源站发生改变时，修改详情列表的属性
        :return:
        """
        details = self.station_id.security_check.plan_detail
        data= []
        for detail in details:
            vals = {
                "security_check_id": self.id,
                "security_check_item_id": detail.id,
                "check_result": 'normal',
                "remarks": ''
            }
            data.append((0, 0, vals))

        self.security_check_detail_ids = data

    @api.multi
    def draft_to_refer(self):
        self.state = 'refer'

    @api.multi
    def refer_to_auditing(self):
        self.state = 'auditing'

    @api.multi
    def refer_to_draft(self):
        self.state = 'draft'

    @api.multi
    def auditing_to_complete(self):
        self.state = 'complete'

    @api.multi
    def auditing_to_refer(self):
        self.state = 'refer'

    @api.multi
    def unlink(self):
        """
            删除数据时判断检查表的状态
        :return:
        """
        for order in self:
            if not  order.state == 'draft':
                raise exceptions.UserError(_('Not draft data cannot be deleted!'))

        return super(security_check,self).unlink()

class security_check_details(models.Model):

    _name = 'energy.security_check_details'
    _description = 'Security Check Details'

    """
        检查详情
    """
    #安全检查
    security_check_id = fields.Many2one('energy.security_check',string='Security Check Id')

    #安全检查项
    security_check_item_id = fields.Many2one('security_manage.check_item',string='Security Check Item Id')

    #检查项目名称
    check_item_name = fields.Char(string='Check Item Name',related='security_check_item_id.check_item_name', store=False, readonly=True)

    #检查内容
    check_content = fields.Char(string='Check Content',related='security_check_item_id.check_content', store=False, readonly=True)

    #检查标准
    check_standards = fields.Char(string='Check Standards',related='security_check_item_id.check_standards', store=False, readonly=True)

    #结果
    check_result = fields.Selection([('normal','Normal'),('abnormal','Abnormal')],string='Check Result')

    #备注
    remarks = fields.Char(string='Remarks')