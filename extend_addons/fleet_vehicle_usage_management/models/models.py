# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time

class FleetVehicle(models.Model):
    """
    车辆档案
    """
    _inherit = "fleet.vehicle"

    warnning = fields.Boolean(compute="_needwarnning")

    def _needwarnning(self):
        for item in self:
            d = item.annual_inspection_date
            if d != False:
                timeArray = time.strptime(d, "%Y-%m-%d")
                timeStamp = int(time.mktime(timeArray))
                currenttime = int(time.time())
                if ( currenttime + 15552000 )> timeStamp :
                    item.warnning = True
                else:
                    item.warnning = False
            else:
                item.warnning = False


class InspectionPlan(models.Model):
    _name = 'fleet_vehicle_usage_management.inspectionplan'

    # 年检计划名称
    planname = fields.Char(string=_('inspection plan name'))
    # 开始日期
    startdate = fields.Date(string=_('inspection start date'))
    # 结束日期
    endtdate = fields.Date(string=_('inspection end date'))
    # 制表日期
    create_date = fields.Datetime(string=_('plan create date'))
    # 审批时间
    approvaldate = fields.Date(string=_('approval date'))
    # 分公司
    branchcompany = fields.Many2one('hr.department', string=_('branch company'))
    # 审批人
    approver = fields.Many2one('res.user', string=_('approver'))
    # 制表人
    maker = fields.Many2one('res.user', string=_('maker'))
    # 备注
    remark = fields.Char(string=_('remark'))
    # 计划详情
    planitem_id = fields.One2many('fleet_vehicle_usage_management.planitem', 'vehicle_id',
                                  string=_("plan detail"))
    # 年检负责人
    principal = fields.Many2one('hr.employee', string=_('inspection principal'))

    state = fields.Selection([
        ('draft',_('draft')),
        ('submitted',_('submitted')),
        ('checked',_('checked')),
        ('execution',_('execution')),
        ('done',_('done')),
    ], string=_('inspection plan state'))

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_submitted(self):
        self.state = 'submitted'

    @api.multi
    def action_checked(self):
        self.state = 'checked'

    @api.multi
    def action_execution(self):
        self.state = 'execution'

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.boss = self._uid

    def generatePlanDetail(self):
        """
        自动填充计划详情列表
        :return:
        """
        pass

class planItem(models.Model):
    _name = 'fleet_vehicle_usage_management.planitem'

    # 年检执行日期
    inspectiondate = fields.Date(string=_('inspection date'))
    # 年检过期日期
    inspectionexpire = fields.Date(string=_('inspection expire'))
    # 备注
    inspectionremark = fields.Date(string=_('inspection remark'))
    # 年检计划
    inspectionplan_id = fields.Many2one('fleet_vehicle_usage_management.inspectionplan',
                                        string=_('inspection plan'))
    # 车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string=_('vehicle info'))
