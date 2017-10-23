# -*- coding: utf-8 -*-
import json
import datetime
import requests
from odoo.exceptions import UserError
from odoo import models, fields, api


def utc2local(str):
    if str:
        local_time = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S') +datetime.timedelta(hours=8)
        return datetime.datetime.strftime(local_time,"%Y-%m-%d %H:%M:%S")


def local2utc(str):
    if str:
        local_time = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S') +datetime.timedelta(hours=-8)
        return datetime.datetime.strftime(local_time,"%Y-%m-%d %H:%M:%S")


class operation_records_move2v3(models.Model):
    _name = 'operation.records.move2v3'
    
    #迁移单编号
    name = fields.Date(required=True)
    #公司
    company_id = fields.Many2one(related='line_id.company_id', readonly=True)
    #开始时间
    start_date = fields.Datetime()
    #结束时间
    end_date = fields.Datetime()    
    #线路
    line_id = fields.Many2one('route_manage.route_manage',required='1')
    #运营理程
    operation_vehicleusage_ids = fields.One2many('vehicleusage.driverecords','record_move_id', domain=[('drivetype','=','working')])
    #非运营理程
    nooperation_vehicleusage_ids = fields.One2many('vehicleusage.driverecords','record_move_id', domain=[('drivetype','!=','working')])
    #签到记录
    attence_record_ids = fields.One2many('employee.attencerecords','record_move_id')
    # 类型
    state = fields.Selection([
        ('draft',u'草稿'), 
        ('syned',u'同步'), 
        ('approved','审核'), 
        ('moved','迁移') 
    ],default="draft", readonly=True)
    move_result = fields.Text()       
    
    
    _sql_constraints = [
        ('name_uniq', 'unique (name,line_id)', u'不能重复迁移同一日期，同一线路的数据!')
    ]
    
    @api.multi
    #审核迁移单    
    def do_approve(self):
        for r in self :
            for operation_vehicleusage_id in r.operation_vehicleusage_ids :
                operation_vehicleusage_id.write({"state":'approved'})
            for nooperation_vehicleusage_id in r.nooperation_vehicleusage_ids :
                nooperation_vehicleusage_id.write({"state":'approved'}) 
            for attence_record_id in r.attence_record_ids :
                attence_record_id.write({"state":'approved'})
        r.write({"state":'approved'})                 
  
    @api.multi
    #通过访问后台提供的restful接口获取到运营理程信息，非运营理程信息和司乘考勤信息    
    def get_data(self):
        driver_recodes_obj = self.env['vehicleusage.driverecords']
        attence_obj = self.env['employee.attencerecords']

        # company_id = self.company_id.id
        start_date = '%s 00:00:00' % (self.name)
        end_data = '%s 23:59:59' % (self.name)
        para_dict = {'lineId': str(self.line_id.id), 'startDate': start_date, 'endDate': end_data}

        # 非运营
        exceptkm_list = driver_recodes_obj.restful_get_data('op_exceptkm', para_dict)
        for data_line in exceptkm_list:
            data_line.update({'record_move_id': self.id})
            line_id = self.env['vehicleusage.driverecords'].create(data_line)

        # 运营
        dispatchplan_list = driver_recodes_obj.restful_get_data('op_dispatchplan', para_dict)
        for data_line in dispatchplan_list:
            data_line.update({'record_move_id': self.id})
            line_id = self.env['vehicleusage.driverecords'].create(data_line)

        # 考勤
        attendance_list = attence_obj.restful_get_data(para_dict)
        for data_line in attendance_list:
            data_line.update({'record_move_id':self.id})
            line_id = self.env['employee.attencerecords'].create(data_line)
        
        self.write({'state':'syned'})

        # values = driver_recodes_obj.restful()
        # driver_recodes_obj.create(values)
        
    @api.multi
    def do_move2V3(self):
        url_config = self.env['ir.config_parameter'].get_param('dispatch.desktop.restful')
        params = {
            'lineId': str(self.line_id.id),
            'type': '0',
            'workDate': self.name
        }

        url = '%s/ltyop/transfer/transferExceptKmOdoo?apikey=71029270&params=%s' % (url_config, json.dumps(dict(params)))
        r = requests.put(url)
        if r.status_code != 200:
            raise UserError((u"连接失败."))

        if r.json().get('result') != 0:
            raise UserError((u"服务器返回查询失败."))
        result =  r.json()['respose']
        self.write({'state':'moved','move_result':result})
        
        

class DriveRecords(models.Model):
    """
    行车记录
    """
    _inherit = 'vehicleusage.driverecords'

    # 公司
    #company_id = fields.Many2one('res.company')
    company_id = fields.Many2one(related='record_move_id.company_id', readonly=True)
    # 线路 route_id
    route_id = fields.Many2one(related='record_move_id.line_id', store=True)
    # 方向 direction
    direction = fields.Selection(
        [('0', u'上行'), ('1', u'下行')])    
    # 日期
    #date = fields.Date()
    date = fields.Date(related='record_move_id.name', readonly=True)
    
    # 计划时间
    date_plan = fields.Datetime()
    # 实际发车时间 realitydepart

    # 计划状态
    state_plan = fields.Selection(
        [(0, u'待发车0'), (1, u'待发车1'), (2, u'已执行'), (3, u'取消')])
    inner_code = fields.Char(related='vehicle_id.inner_code', readonly=True)
    # 司机工号 driver_id

    # 司机姓名
    driver_name = fields.Char(related='driver_id.name', readonly=True)
    # 计划到达时间 planarrive

    # 实际到达时间 realityarrive

    # 运营时长
    time_operation = fields.Float()
    # 计划公理数 planmileage

    # GPS公理数 GPSmileage

    # 运营属性
    operation_att = fields.Selection([('0', u'正常'), ('1', u'包车')])

    # 异常
    abnormal = fields.Selection(
        [('2003', u'进出场'), ('2002', u'加油加气'), ('2005', u'故障'), ('2006', u'保养'), ('2004', u'空放'), ('2001', u'其他'), ('0', u'否'), ('1', u'是')])

    # 生成日期
    gen_date = fields.Datetime()
    # 是否补录
    is_add = fields.Boolean(default=True, readonly=True)
    # 备注
    note = fields.Char()
    #移转单ID
    record_move_id = fields.Many2one('operation.records.move2v3')
    # 类型
    state = fields.Selection([
        ('draft',u'草稿'), 
        ('approved','审核'), 
        ('moved','迁移') 
    ],default="draft", readonly=True)


    # restful_key_id
    restful_key_id = fields.Char()

    finish_state = fields.Selection([('1', u'运行中'),('2', u'已完成')])

    _sql_constraints = [
        ('restful_key_id_record_move_id', 'unique (record_move_id,restful_key_id)', u'不能重复迁移同一日期的数据!')
    ]


    @api.multi
    def restful_get_data(self, type, search_para):
        url_config = self.env['ir.config_parameter'].get_param('dispatch.desktop.restful')

        params = {
            'tablename': type,
            'pageNum': '1',
            'pageSize': '1000000'
        }

        url = '%s/ltyop/planData/queryListByPage?apikey=71029270&params=%s' % (url_config, json.dumps(dict(params, **search_para)))
        r = requests.get(url)
        if r.status_code != 200:
            raise UserError((u"查询失败."))

        if r.json().get('result') != 0:
            raise UserError((u"服务器返回查询失败."))


        if type == 'op_exceptkm':      # 非运营
            data_list = []
            for item in r.json()['respose']['list']:
                if self.env['fleet.vehicle'].search([('on_boardid', '=', item.get('onBoardId'))]) :
                    on_boardid = self.env['fleet.vehicle'].search([('on_boardid', '=', item.get('onBoardId'))])[0].id
                else:
                    raise UserError((u"车辆不存在."))

                new_data = {
                    'restful_key_id': item.get('id'),

                    'company_id': int(item.get('companyId')),  # 公司
                    'route_id': item.get('lineId'),     # 线路
                    'vehicle_id': on_boardid,  # 车辆
                    # 'driver_id': int(item.get('driverName')),  # 司机
                    # 司机姓名

                    'date': local2utc(item.get('createTime', '')).split(' ')[0] or None,   # todo
                    'realitydepart': local2utc(item.get('startTime')) or None,     # 开始时间
                    'realityarrive': local2utc(item.get('endTime')) or None,      # 结束时间

                    'abnormal': str(item.get('kmTypeId')),

                    'planmileage': item.get('planKm'),         # 计划里程数
                    'GPSmileage': item.get('realKm'),          # GPS里程数
                    'gen_date': local2utc(item.get('createTime')) or None,        # 生成时间
                    # 'finish_state': item.get('finishState'),   # 状态

                    'note': item.get('remark'),  # String	备注

                    'is_add': False,
                    'state': 'draft',
                    'drivetype': 'empty',
                    # item.get('addReason')  # int	添加原因id
                    # item.get('companyName')  # Int	公司名称
                    # item.get('gprsId')  # Int	线路编码
                    #
                    # item.get('isManual')  # Int	是否手动处理（0：否，1：是）
                    # item.get('kmTypeName')  # String	异常名称
                    #
                    # item.get('endKm'),  # tring	结束公里
                    # item.get('startKm')  # Double	开始里程
                }

                data_list.append(new_data)
            return data_list
        # 运营里程
        elif type == 'op_dispatchplan':
            data_list = []
            for item in r.json()['respose']['list']:
                if self.env['fleet.vehicle'].search([('on_boardid', '=', item.get('onBoardId'))]):
                    vehicle_id = self.env['fleet.vehicle'].search([('on_boardid', '=', item.get('onBoardId'))])[0].id
                else:
                    raise UserError((u"车辆不存在."))

                if self.env['hr.employee'].search([('jobnumber', '=', item.get('workerId'))]):
                    driver_id = self.env['hr.employee'].search([('jobnumber', '=', item.get('workerId'))])[0].id
                else:
                    driver_id = None

                new_data = {
                    'restful_key_id': item.get('id'),
                    # 'company_id': int(item.get('companyId')) or None,  # 公司
                    'route_id': item.get('lineId'),  # 线路
                    'direction': str(item.get('direction')),  # 方向

                    # 'date': local2utc(item.get('createTime', '')).split(' ')[0] or None,  # 日期
                    'date_plan': local2utc(item.get('planRunTime')),  # 计划时间：
                    'realitydepart': local2utc(item.get('realRunTime')) or None,   # 实际发车时间
                    'state_plan': item.get('planState'),  # 计划状态
                    'vehicle_id': vehicle_id,  # 车辆编号

                    'driver_id': driver_id,    # 司机ID
                    'planarrive': local2utc(item.get('planReachTime')),   # 计划到达时间
                    'realityarrive': item.get('realReachTime') or None,  # 实际到达时间

                    # 计划公里数
                    'planmileage': item.get('planKm'),         # 计划里程数
                    # GPS公里数
                    # 'GPSmileage': item.get('realKm'),          # GPS里程数

                    'operation_att': str(item.get('addType')),  # 运营属性
                    # 异常
                    'abnormal': str(item.get('isExcept')),        # 异常

                    # 生成日期
                    'gen_date': local2utc(item.get('createTime')) or None,        # 生成时间

                    # 备注
                    # 'note': item.get('remark'),  # String    备注
                    # 是否手动增加
                    'is_add': False,
                    # 同步成功后的状态
                    'state': 'draft',
                    # 类型
                    'drivetype': 'working',

                    # 'driver_id': int(item.get('driverName')),  # 司机
                    # 司机姓名
                    # 'finish_state': item.get('finishState'),   # 状态
                    # item.get('addReason')  # int    添加原因id
                    # item.get('companyName')  # Int    公司名称
                    # item.get('gprsId')  # Int    线路编码
                    #
                    # item.get('isManual')  # Int    是否手动处理（0：否，1：是）
                    # item.get('kmTypeName')  # String    异常名称
                    #
                    # item.get('endKm'),  # tring    结束公里
                    # item.get('startKm')  # Double    开始里程
                }

                data_list.append(new_data)
            return data_list


class attence(models.Model):
    """
    考勤记录
    """
    _inherit = 'employee.attencerecords'

    # 公司
    #company_id = fields.Many2one('res.company')
    company_id = fields.Many2one(related='record_move_id.company_id', readonly=True)
    # 线路 route_id
    line_id = fields.Many2one(related='record_move_id.line_id', store=True)
    # 员工 employee_id

    # 车辆
    vehicle_id = fields.Many2one('fleet.vehicle')
    # 日期
    date = fields.Date()
    #移转单ID
    record_move_id = fields.Many2one('operation.records.move2v3')
    
    # 签到时间 checkingin

    # 签退时间 checkinginout
    #是否客户端补录
    is_add = fields.Boolean(default=True, readonly=True)
    # 类型
    state = fields.Selection([
        ('draft',u'草稿'), 
        ('approved','审核'), 
        ('moved','迁移') 
    ],default="draft", readonly=True)

    @api.multi
    def restful_get_data(self, search_para):
        url_config = self.env['ir.config_parameter'].get_param('dispatch.desktop.restful')

        params = {
            'tablename': 'op_attendance',
            'pageNum': '1',
            'pageSize': '1000000'
        }

        url = '%s/ltyop/planData/queryListByPage?apikey=71029270&params=%s' % (url_config, json.dumps(dict(params, **search_para)))
        r = requests.get(url)
        if r.status_code != 200:
            raise UserError((u"查询失败."))

        if r.json().get('result') != 0:
            raise UserError((u"服务器返回查询失败."))

        data_list = []
        for item in r.json()['respose']['list']:
            if self.env['fleet.vehicle'].search([('on_boardid', '=', item.get('onBoardId'))]):
                on_boardid = self.env['fleet.vehicle'].search([('on_boardid', '=', item.get('onBoardId'))])[0].id
            else:
                raise UserError((u"车辆不存在."))

            if self.env['hr.employee'].search([('jobnumber', '=', item.get('workerId'))]):
                employee_id = self.env['hr.employee'].search([('jobnumber', '=', item.get('workerId'))])[0].id
            else:
                raise UserError((u"员工不存在."))

            new_data = {
                'company_id': '',
                'line_id': item.get('lineId'),                                  # 线路ID 27,
                'vehicle_id': on_boardid,
                'employee_id': employee_id,                                     # workerId "15373",
                'date': item.get('workDate').split(' ')[0] or None,             # 工作日期 "2017-10-19 00:00:00",
                'checkingin': local2utc(item.get('conWorkTime')) or None,       #  "签到时间",
                'checkinginout': local2utc(item.get('coffWorkTime')) or None,   # "签退时间",
                'is_add': False,

                # : item.get('dispatchPlanId'],		#  -1,
                # : item.get('driverName'],			#  "司机姓名 15373",
                # : item.get('gprsId'],				#  线路编码 251,
                # : item.get('id'],				    #  2428,
                #
                # : item.get('offWorkBus'],			#  "",
                # : item.get('onBoardId'],			#   15378,
                # : item.get('onWorkBus'],			#  "上班车辆",
                # :
                # : item.get('orderNo'],				#  0,
                # : item.get('planReachTime'],		#  "",
                # : item.get('planRunTime'],			#  "",
                # : item.get('planTime'],			    #  "",
                # : item.get('remark'],				#  "",
                # : item.get('selfId'],				#  "",
                # : item.get('workTime'],			    #  "",
                # : item.get('workerType'],			#  workerType 1019
            }

            data_list.append(new_data)
        return data_list

