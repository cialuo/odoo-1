# -*- coding: utf-8 -*-
import json
import datetime
import requests
from odoo.exceptions import UserError
from odoo import models, fields, api


class operation_records_move2v3(models.Model):
    _name = 'operation.records.move2v3'
    
    #迁移单编号
    name = fields.Date(required=True)
    #公司
    company_id = fields.Many2one('res.company')
    #开始时间
    start_date = fields.Datetime()
    #结束时间
    end_date = fields.Datetime()    
    #线路
    line_id = fields.Many2one('route_manage.route_manage')
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
        data_list = driver_recodes_obj.restful_get_data('op_exceptkm', para_dict)
        for data_line in data_list :
            data_line.update({'record_move_id':self.id})
            line_id = self.env['vehicleusage.driverecords'].create(data_line)

        # # 运营
        # r = driver_recodes_obj.restful_get_data('op_dispatchplan', para_dict)
        #
        # # 考勤
        # r = attence_obj.restful_get_data(para_dict)


        # values = driver_recodes_obj.restful()
        # driver_recodes_obj.create(values)

class DriveRecords(models.Model):
    """
    行车记录
    """
    _inherit = 'vehicleusage.driverecords'

    # 公司
    company_id = fields.Many2one('res.company')
    # 线路 route_id
    # 方向 direction
    # 日期
    date = fields.Date()
    # 计划时间
    date_plan = fields.Datetime()
    # 实际发车时间 realitydepart

    # 计划状态
    state_plan = fields.Char()
    # 车辆编号
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
    operation_att = fields.Char()
    # 异常
    abnormal = fields.Selection(
        [('2003', u'进出场'), ('2002', u'加油加气'), ('2005', u'故障'), ('2006', u'保养'), ('2004', u'空放'), ('2001', u'其他')])

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
                    'route_id': item.get('lineName'),     # 线路
                    'vehicle_id': on_boardid,  # 车辆
                    # 'driver_id': int(item.get('driverName')),  # 司机
                    # 司机姓名

                    'date': item.get('createTime', '').split(' ')[0] or None,   # todo
                    'realitydepart': item.get('startTime') or None,     # 开始时间
                    'realityarrive': item.get('endTime') or None,      # 结束时间

                    'abnormal': str(item.get('kmTypeId')),          # 异常类型

                    'planmileage': item.get('planKm'),         # 计划里程数
                    'GPSmileage': item.get('realKm'),          # GPS里程数
                    'gen_date': item.get('createTime') or None,        # 生成时间
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

        elif type == 'op_dispatchplan':
            for item in r.json()['respose']['list']:
                pass

class attence(models.Model):
    """
    考勤记录
    """
    _inherit = 'employee.attencerecords'

    # 公司
    company_id = fields.Many2one('res.company')
    # 线路
    line_id = fields.Many2one('route_manage.route_manage')
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

