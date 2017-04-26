# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from odoo.exceptions import ValidationError
import  datetime
import odoo.tools.misc
class FleetVehicle(models.Model):
    """
    车辆档案
    """
    _inherit = "fleet.vehicle"

    # 是否报警
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
    name = fields.Char(string=_('inspection plan name'), required=True)
    # 开始日期
    startdate = fields.Date(string=_('inspection start date'), required=True)
    # 结束日期
    enddate = fields.Date(string=_('inspection end date'), required=True)
    # 制表日期
    create_date = fields.Datetime(string=_('plan create date'))
    # 审批时间
    approvaldate = fields.Datetime(string=_('approval date'))
    # 分公司
    branchcompany = fields.Many2one('hr.department', string=_('branch company'), required=True)
    # 审批人
    approver = fields.Many2one('res.users', string=_('approver'))
    # 制表人
    maker = fields.Many2one('res.users', string=_('maker'), default=lambda self: self._uid)

    # 备注
    remark = fields.Char(string=_('remark'))
    # 计划详情
    planitem_id = fields.One2many('fleet_vehicle_usage_management.planitem', 'inspectionplan_id',
                                  string=_("plan detail"))
    # 年检计划
    subject = fields.Char(string=_('plan subject'))

    # 年检负责人
    principal = fields.Many2one('hr.employee', string=_('inspection principal'))

    # 状态表
    state = fields.Selection([
        ('draft',_('draft')),           # 草稿
        ('submitted',_('submitted')),   # 已提交
        ('checked',_('checked')),       # 已审批
        ('execution',_('execution')),   # 执行中
        ('done',_('done')),             # 已完成
    ], string=_('inspection plan state'),default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_submitted(self):
        self.state = 'submitted'

    @api.multi
    def action_checked(self):
        self.state = 'checked'
        self.approver = self._uid
        self.approvaldate = datetime.datetime.now().strftime(odoo.tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)

    @api.multi
    def action_execution(self):
        self.state = 'execution'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def generatePlanDetail(self):
        """
        自动填充计划详情列表
        """
        vehiclemode = self.env['fleet.vehicle']
        for item in self:
            startdate = item.startdate
            enddate = item.enddate
            externdate = time.strftime("%Y-%m-%d",
                                       time.localtime(time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 7776000))

            vehiclelist = vehiclemode.search(
                [
                    ('annual_inspection_date', '>=', startdate),
                    ('annual_inspection_date', '<=', externdate)
                ]
            )
            items = []
            for v in vehiclelist:
                if self.hasItem(v.id)>0:
                    continue
                value = {
                    'state' : 'execution',
                    'vehicle_id' :v.id
                }
                items.append((0,0,value))
            item.write({'planitem_id':items})
        return True

    # 已添加年检单的车辆不能再次被加入到计划单
    def hasItem(self, vehicleid):
        planitemmode = self.env['fleet_vehicle_usage_management.planitem']
        count = planitemmode.search_count([
            ('state','=','execution'),
            ('vehicle_id','=',vehicleid)
        ])
        return count

    @api.model
    def create(self, vals):
        res = super(InspectionPlan, self).create(vals)
        planItems = vals.get('planitem_id', [])
        for item in planItems:
            if item[0] == 0 or (item[0] == 1 and item[2].has_key('vehicle_id')):
                if self.hasItem(item[2]['vehicle_id']) > 1:
                    raise ValidationError(_("there is a vehicle that already have inspection plan "))
        return res

    @api.multi
    def write(self, vals):
        res = super(InspectionPlan, self).write(vals)
        planItems = vals.get('planitem_id', [])
        for item in planItems:
            if item[0] == 0 or (item[0] == 1 and item[2].has_key('vehicle_id')):
                if self.hasItem(item[2]['vehicle_id'])>1:
                    raise ValidationError(_("there is a vehicle that already have inspection plan "))
        return res


class PlanItem(models.Model):

    _name = 'fleet_vehicle_usage_management.planitem'


    # 车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string=_('vehicle info'), required=True)

    # 内部编号
    inner_code = fields.Char(related='vehicle_id.inner_code', readonly=True)
    # 车牌号
    license_plate = fields.Char(related='vehicle_id.license_plate', readonly=True)
    # 隶属公司
    company_id = fields.Many2one(related='vehicle_id.company_id', readonly=True)
    # 线路
    route_id = fields.Many2one(related='vehicle_id.route_id', readonly=True)
    # 年检到期
    annual_inspection_date = fields.Date(related='vehicle_id.annual_inspection_date', readonly=True)
    # 状态表
    state = fields.Selection([
        ('execution', _('execution')),  # 进行中
        ('done', _('done')),            # 已完成
    ], string=_('plan item state'), default='execution')

    # 年检计划
    inspectionplan_id = fields.Many2one('fleet_vehicle_usage_management.inspectionplan',
                                        string=_('inspection plan'),ondelete='cascade')

    # 送检司机
    inspectiondriver = fields.Char(string=_('inspection driver'))
    # 计划日期
    plandate = fields.Date(string=_('plan to inspection date'))
    # 实际年检日期
    actualdate = fields.Date(string=_('actual inspection date'))

class InspectionRecords(models.Model):
    """
    年检结果表
    """

    _name = 'fleet_vehicle_usage_management.inspectionrecords'

    # 年检执行日期
    inspectiondate = fields.Date(string=_('inspection date'))
    # 年检过期日期
    inspectionexpire = fields.Date(string=_('inspection expire'))
    # 备注
    inspectionremark = fields.Date(string=_('inspection remark'))

    # 车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string=_('vehicle info'))

    # 内部编号
    inner_code = fields.Char(related='vehicle_id.inner_code', readonly=True)
    # 车牌号
    license_plate = fields.Char(related='vehicle_id.license_plate', readonly=True)
    # 登记证号
    reg_no = fields.Char(related='vehicle_id.reg_no', readonly=True)
    # 登记日期
    reg_date = fields.Date(related='vehicle_id.reg_date', readonly=True)
    # 强制报废
    forced_destroy = fields.Char(related='vehicle_id.forced_destroy', readonly=True)
    # 隶属公司
    company_id = fields.Many2one(related='vehicle_id.company_id', readonly=True)
    # 线路
    route_id = fields.Many2one(related='vehicle_id.route_id', readonly=True)


class VehicleAnchor(models.Model):
    _name = 'fleet_vehicle_usage_management.VehicleAnchor'

    # 关联的车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string=_('vehicle info'), required=True)
    # 内部编号
    inner_code = fields.Char(related='vehicle_id.inner_code', readonly=True)
    # 车牌号
    license_plate = fields.Char(related='vehicle_id.license_plate', readonly=True)
    # 车型
    model_id = fields.Many2one(related='vehicle_id.model_id', readonly=True)
    # 隶属公司
    company_id = fields.Many2one(related='vehicle_id.company_id', readonly=True)
    # 线路
    route_id = fields.Many2one(related='vehicle_id.route_id', readonly=True)
    # 抛锚时间
    anchortime = fields.datetime(string=_('anchor time'))
    # 抛锚路段
    anchorroad = fields.Char(string=_('anchor road'))
    # 抛锚原因
    anchorreason = fields.Char(string=_('anchor reason'))
