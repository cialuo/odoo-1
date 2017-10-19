# -*- coding: utf-8 -*-

from odoo import models, fields, api, _,exceptions
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
                if ( currenttime + 7776000 )> timeStamp :   # 三个月内年检到期就标红
                    item.warnning = True
                else:
                    item.warnning = False
            else:
                item.warnning = False

    # 行车记录
    driverecords = fields.One2many('vehicleusage.driverecords', 'vehicle_id', string="drive records")

    # 年检状态
    inspectionState = fields.Char(compute='_getInspectionState', string="vehicle inspection state")

    # 到期天数
    deadlinedays = fields.Integer(compute="_deadlinedays", string="dead line days")

    @api.multi
    def _deadlinedays(self):
        for item in self:
            today = datetime.datetime.today()
            if item.annual_inspection_date:
                item.deadlinedays = (datetime.datetime.strptime(item.annual_inspection_date, "%Y-%m-%d")-today).days



    def getPlanItem(self, vid):
        item = self.env['vehicle_usage.planitem']
        vechileinfo = item.search([('vehicle_id', '=', vid),('state', '=', 'execution')], limit=1)
        if len(vechileinfo) == 0:
            return False
        else:
            return vechileinfo[0]

    @api.multi
    def _getInspectionState(self):
        for item in self:
            #planitem = self.env['vehicle_usage.planitem']
            #count = planitem.search_count([('vehicle_id', '=', item.id), ('state', '=', 'execution')])
            if item.deadlinedays > 0:
                item.inspectionState = _('checking')
            elif item.deadlinedays < 0:
                item.inspectionState = _('expired')
            else:
                item.inspectionState = _('checking done')

class InspectionPlan(models.Model):
    _name = 'vehicle_usage.inspectionplan'

    # 年检计划名称
    name = fields.Char(string="inspection plan name", required=True)
    # 开始日期
    startdate = fields.Date(string="inspection start date", required=True)
    # 结束日期
    enddate = fields.Date(string="inspection end date", required=True)
    # 制表日期
    create_date = fields.Datetime(string="plan create date")
    # 审批时间
    approvaldate = fields.Datetime(string="approval date")
    # 分公司
    branchcompany = fields.Many2one('hr.department', string="branch company", required=True)
    # 审批人
    approver = fields.Many2one('res.users', string="approver")
    # 制表人
    maker = fields.Many2one('res.users', string="maker", default=lambda self: self._uid)

    # 备注
    remark = fields.Char(string="remark")
    # 计划详情
    planitem_id = fields.One2many('vehicle_usage.planitem', 'inspectionplan_id',
                                  string="plan detail")
    # 年检计划
    subject = fields.Char(string="plan subject")

    # 年检负责人
    principal = fields.Many2one('hr.employee', string="inspection principal")

    # 状态表
    state = fields.Selection([
        ('draft','draft'),           # 草稿
        ('submitted','submitted'),   # 已提交
        ('checked','checked'),       # 已审批
        ('execution','execution'),   # 执行中
        ('done','done'),             # 已完成
    ], string="inspection plan state",default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_submitted(self):

        """
            新增验证：
                在提交时验证是否存在详情
        :return:
        """
        if len(self.planitem_id) == 0:
            raise exceptions.UserError(_('Annual inspection details can not be empty.'))

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
            companyid = item.branchcompany
            externdate = time.strftime("%Y-%m-%d",
                                       time.localtime(time.mktime(time.strptime(enddate, "%Y-%m-%d")) + 7776000))

            vehiclelist = vehiclemode.search(
                [
                    ('annual_inspection_date', '>=', startdate),
                    ('annual_inspection_date', '<=', externdate),
                    ('company_id', '=', companyid.id),
                    ('vehicle_life_state', '=', 'operation_period')
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

    @api.constrains('startdate', 'enddate')
    def _check_inspectionexpire(self):
        """
            2017年7月26日 新增验证：
                年检过期时间不能小于年检日期
        :return:
        """
        for order in self:
            if order.startdate > order.enddate:
                raise exceptions.ValidationError(_("Inspectionexpire can not be greater than the inspectiondate"))

class PlanItem(models.Model):

    _name = 'vehicle_usage.planitem'

    # 车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string="vehicle info", required=True,domain=[('entry_state','=','audited'),('vehicle_life_state','=','operation_period')])

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
        ('execution', 'execution'),  # 进行中
        ('done', 'done'),            # 已完成
    ], string="plan item state", default='execution')

    # 年检计划
    inspectionplan_id = fields.Many2one('vehicle_usage.inspectionplan',
                                        string="inspection plan",ondelete='cascade')

    # 送检司机
    inspectiondriver = fields.Char(string="inspection driver")
    # 计划日期
    plandate = fields.Date(string="plan to inspection date")
    # 实际年检日期
    actualdate = fields.Date(string="actual inspection date")



class InspectionRecords(models.Model):
    """
    年检结果表
    """

    _name = 'vehicle_usage.inspectionrecords'

    _rec_name = 'inner_code'

    # 年检执行日期
    inspectiondate = fields.Date(string="inspection date", required=True)
    # 年检过期日期
    inspectionexpire = fields.Date(string="inspection expire", required=True)
    # 备注
    inspectionremark = fields.Char(string="inspection remark")

    # 车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string="vehicle info", required=True,domain=[('entry_state','=','audited')])

    # 内部编号
    inner_code = fields.Char(related='vehicle_id.inner_code')
    # 总里程
    total_odometer = fields.Float(related='vehicle_id.total_odometer')
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

    # 到期日期
    annual_inspection_date = fields.Date(string="inspection end date")

    #2017年7月25日 新增字段：年检记录状态
    state = fields.Selection([('draft', "draft"),('passed', "passed")],string='Inspection state',default='draft')

    @api.multi
    def action_draft_to_passed(self):
        """
            年检记录状态：草稿-->已通过
            更新车辆年检的到期时间
            更新车辆年检计划的状态
        :return:
        """
        self.state = 'passed'

        #更新车辆的年检到期时间
        if self.vehicle_id:

            self.vehicle_id.annual_inspection_date = self.inspectionexpire
            #更新车辆年检计划
            planItem = self.getPlanItem(self.vehicle_id.id)
            if planItem:
                planItem.write({'state': 'done', 'actualdate': self.inspectionexpire})
                inspectionplan = planItem.inspectionplan_id
                if inspectionplan.planitem_id.mapped('state').count('done') == len(inspectionplan.planitem_id):
                    inspectionplan.state = 'done'

    @api.constrains('inspectiondate', 'inspectionexpire')
    def _check_inspectionexpire(self):
        """
            2017年7月26日 新增验证：
                年检过期时间不能小于年检日期
        :return:
        """
        for order in self:
            if order.inspectiondate > order.inspectionexpire:
                raise exceptions.ValidationError(_("Inspectionexpire can not be greater than the inspectiondate"))


    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        self.annual_inspection_date = self.vehicle_id.annual_inspection_date


    def getVehicleIdByInnercode(self, code):
        vehicle = self.env['fleet.vehicle']
        vechileinfo = vehicle.search([('inner_code', '=', code)], limit=1)
        if len(vechileinfo) == 0:
            return False
        else:
            return vechileinfo[0]

    def getVehicleIdById(self, id):
        vehicle = self.env['fleet.vehicle']
        vechileinfo = vehicle.search([('id', '=', id)], limit=1)
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
                    self.buidMessage(message=_('inner code not exist %s ') % innerCode,
                                     moreinfo=_('can not found inner code %s in system ') % innerCode)
                )
                return returnVal

        res = super(InspectionRecords, self).load(fields, data)
        return res

    def getPlanItem(self, vid):
        item = self.env['vehicle_usage.planitem']
        vechileinfo = item.search([('vehicle_id', '=', vid),('state', '=', 'execution')], limit=1)
        if len(vechileinfo) == 0:
            return False
        else:
            return vechileinfo[0]

    @api.model
    def create(self, vals):

        #if vals.get('vehicle_id',None) != None:
        #    vehicleinfo = self.getVehicleIdById(vals['vehicle_id'])
        #elif vals.get('inner_code', None) != None:
        #    vehicleinfo = self.getVehicleIdByInnercode(vals['inner_code'])
        #vals['vehicle_id'] = vehicleinfo['id']
        #vals['annual_inspection_date'] = vehicleinfo.annual_inspection_date
        #vehicleinfo.write({'annual_inspection_date':vals['inspectionexpire']})

        res = super(InspectionRecords, self).create(vals)
        #planItem = self.getPlanItem(vehicleinfo['id'])
        #if planItem!=False:
            #planItem.write({'state':'done','actualdate':vals['inspectiondate']})
        return res


class DriveRecords(models.Model):
    """
    行车记录
    """
    _name = 'vehicleusage.driverecords'

    # 所属日期
    relateddate = fields.Date(string="mileage data")

    # 关联的车辆信息
    vehicle_id = fields.Many2one('fleet.vehicle', string="vehicle info", required=True)
    # 线路
    route_id = fields.Many2one(related='vehicle_id.route_id', readonly=True)
    # 车牌号
    license_plate = fields.Char(related='vehicle_id.license_plate', readonly=True)
    # 司机
    driver_id = fields.Many2one('hr.employee', string="driver")
    # 方向
    direction = fields.Char(string="drive direction")
    # 计划里程
    planmileage = fields.Float(string="plan mileage")
    # GPS里程
    GPSmileage = fields.Float(string="GPS mileage")
    # 趟次
    dirvetimes = fields.Char(string="drive times")
    # 计划发车
    plandepart = fields.Datetime(string="plan depart")
    # 实际发车
    realitydepart = fields.Datetime(string="reality depart")
    # 计划到达
    planarrive = fields.Datetime(string="plan arrive")
    # 实际到达
    realityarrive = fields.Datetime(string="reality arrive")
    # 类型
    drivetype = fields.Selection([
        ('working','drive type working'),    # 运营
        ('refuel','drive type refuel'),      # 加油
        ('empty','drive type empty')         # 空驶
    ],string="drive type")


    @api.model
    def create(self, vals):
        res = super(DriveRecords, self).create(vals)
        odometer = self.env['fleet.vehicle.odometer']
        vechileinfo = odometer.search([('vehicle_id', '=', vals['vehicle_id'])], limit=1)
        if len(vechileinfo) > 0:
            instance = vechileinfo[0]
            instance.write({'value':instance.value+vals['GPSmileage']})
        return res






