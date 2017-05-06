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

    # 行车记录
    driverecords = fields.One2many('vehicleusage.driverecords', 'vehicle_id', string=_('drive records'))
    # 抛锚记录


class InspectionPlan(models.Model):
    _name = 'vehicle_usage.inspectionplan'

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
    planitem_id = fields.One2many('vehicle_usage.planitem', 'inspectionplan_id',
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
        planitemmode = self.env['vehicle_usage.planitem']
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

    _name = 'vehicle_usage.planitem'

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
    inspectionplan_id = fields.Many2one('vehicle_usage.inspectionplan',
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

    _name = 'vehicle_usage.inspectionrecords'

    _rec_name = 'inner_code'

    # 年检执行日期
    inspectiondate = fields.Date(string=_('inspection date'))
    # 年检过期日期
    inspectionexpire = fields.Date(string=_('inspection expire'))
    # 备注
    inspectionremark = fields.Char(string=_('inspection remark'))

    # 车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string=_('vehicle info'))

    # 内部编号
    inner_code = fields.Char(related='vehicle_id.inner_code')
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

    def getVehicleIdByInnercode(self, code):
        vehicle = self.env['fleet.vehicle']
        vechileinfo = vehicle.search([('inner_code', '=', code)], limit=1)
        if len(vechileinfo) == 0:
            return False
        else:
            return vechileinfo[0]

    def buidMessage(self, type='error', message='', moreinfo=''):
        return dict(
            {'record': 0, 'rows': {'to': 0, 'from': 0}},
            type=type, message=message,
            moreinfo=moreinfo
        )

    @api.model
    def load(self, fields, data):
        returnVal = {'ids': False, 'messages': []}
        if 'inspectiondate' not in fields:
            returnVal['messages'].append(
                self.buidMessage(message=_('need inspection date'),
                                 moreinfo=_('must have inspection date in data file'))
            )
            return returnVal
        elif 'inspectionexpire' not in fields:
            returnVal['messages'].append(
                self.buidMessage(message=_('need inspection expire date'),
                                 moreinfo=_('must have inspection expire date in data file'))
            )
            return returnVal
        elif 'inner_code' not in fields:
            returnVal['messages'].append(
                self.buidMessage(message=_('need inner code'),
                                 moreinfo=_('must have inner code in data file'))
            )
            return returnVal
        for item in data:
            record = dict(zip(fields,item))
            innerCode = record.get('inner_code', None)
            vehicleinfo = self.getVehicleIdByInnercode(innerCode)
            if vehicleinfo == False:
                returnVal['messages'].append(
                    self.buidMessage(message=_('inner code not exist %s ' % innerCode),
                                     moreinfo=_('can not found inner code %s in system ' % innerCode))
                )
                return returnVal

        res = super(InspectionRecords, self).load(fields, data)
        return res

    def getPlanItem(self, vid):
        item = self.env['vehicle_usage.planitem']
        vechileinfo = item.search([('vehicle_id', '=', vid),('state', '<=', 'execution')], limit=1)
        if len(vechileinfo) == 0:
            return False
        else:
            return vechileinfo[0]

    @api.model
    def create(self, vals):
        vehicleinfo = self.getVehicleIdByInnercode(vals['inner_code'])
        vals['vehicle_id'] = vehicleinfo['id']
        vehicleinfo.write({'annual_inspection_date':vals['inspectionexpire']})
        res = super(InspectionRecords, self).create(vals)
        planItem = self.getPlanItem(vehicleinfo['id'])
        if planItem!=False:
            planItem.write({'state':'done','actualdate':vals['inspectiondate']})
        return res


class DriveRecords(models.Model):
    """
    行车记录
    """
    _name = 'vehicleusage.driverecords'

    # 关联的车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string=_('vehicle info'), required=True)
    # 线路
    route_id = fields.Many2one(related='vehicle_id.route_id', readonly=True)
    # 车牌号
    license_plate = fields.Char(related='vehicle_id.license_plate', readonly=True)
    # 司机
    driver_id = fields.Many2one('hr.employee', string=_('driver'))
    # 方向
    direction = fields.Char(string=_('drive direction'))
    # 计划里程
    planmileage = fields.Float(string=_('plan mileage'))
    # GPS里程
    GPSmileage = fields.Float(string=_('GPS mileage'))
    # 趟次
    dirvetimes = fields.Char(string=_('drive times'))
    # 计划发车
    plandepart = fields.Datetime(string=_('plan depart'))
    # 实际发车
    realitydepart = fields.Datetime(string=_('reality depart'))
    # 计划到达
    planarrive = fields.Datetime(string=_('plan arrive'))
    # 实际到达
    realityarrive = fields.Datetime(string=_('reality arrive'))
    # 类型
    drivetype = fields.Selection([
        ('working',_('drive type working')),    # 运营
        ('refuel',_('drive type refuel')),      # 加油
        ('empty',_('drive type empty'))         # 空驶
    ],string=_('drive type'))


    @api.model
    def create(self, vals):
        res = super(DriveRecords, self).create(vals)
        odometer = self.env['fleet.vehicle.odometer']
        vechileinfo = odometer.search([('vehicle_id', '=', vals['vehicle_id'])], limit=1)
        if len(vechileinfo) > 0:
            instance = vechileinfo[0]
            instance.write({'value':instance.value+vals['GPSmileage']})
        return res
