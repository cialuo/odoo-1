# -*- coding: utf-8 -*-

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
    operation_vehicleusage_ids = fields.One2many('vehicleusage.driverecords','record_move_id')
    #非运营理程
    nooperation_vehicleusage_ids = fields.One2many('vehicleusage.driverecords','record_move_id')
    #签到记录
    attence_record_ids = fields.One2many('employee.attencerecords','record_move_id')
    
    _sql_constraints = [
        ('name_uniq', 'unique (name,line_id)', u'不能重复迁移同一日期，同一线路的数据!')
    ]
    
    
    @api.multi
    #通过访问后台提供的restful接口获取到运营理程信息，非运营理程信息和司乘考勤信息    
    def get_data(self):
        company_id = self.company_id.id
        start_date = self.start_date
        #driver_recodes_obj = self.env['vehicleusage.driverecords']
        #attence_obj = self.env['employee.attencerecords']
        #values = driver_recodes_obj.restful()
        #driver_recodes_obj.create(values)
        
        

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
    abnormal = fields.Char()
    # 生成日期
    gen_date = fields.Datetime()
    # 是否补录
    is_add = fields.Boolean()
    # 备注
    note = fields.Char()
    #移转单ID
    record_move_id = fields.Many2one('operation.records.move2v3')
    

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

