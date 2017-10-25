# -*- coding: utf-8 -*-
##############################################################################
#
#
#    Copyright (C) 2017 xiao (715294035@qq.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.
#
##############################################################################
from odoo import api, fields, models
from extend_addons.lty_dispatch_restful.core.restful_client import *
from odoo.exceptions import RedirectWarning, UserError, ValidationError
import mapping
import datetime
import logging

#对接系统  用户表管理
#运营表
TABLE_work = 'operate'
#非运营表
TABLE_others = 'nonOperate'

_logger = logging.getLogger(__name__)
class DriveRecords(models.Model):

    _inherit = 'vehicleusage.driverecords'

    '''
        继承行车记录管理理,调用restful api
    '''

    @api.model
    def create(self, vals):
        '''
            数据创建完成调用api
        :param vals:
        :return:
        '''
        #根据drivetype类型判断调用哪个表
        if vals.get('drivetype') == 'working' :
            TABLE = TABLE_work
        else :
            TABLE = TABLE_others

        res = super(DriveRecords, self).create(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        #当本地添加时，调用api同步数据到后台
        if  vals.get('is_add') :
            _logger.info('Start create data: %s', self._name)
            vals = mapping.dict_transfer(self._name, vals)
            vals.update({
                'line':res.route_id.line_name,
                'selfId':res.vehicle_id.inner_code,
                'onBoardId':int(res.vehicle_id.on_boardid),
                'gprsId':res.route_id.gprs_id,
                'workerId':res.driver_id.jobnumber,
                'driver':res.driver_id.name,
            })
            params = Params(type=1, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
            #调用restful
            rp = Client().http_post(url, data=params)
            if rp :
                restful_key_id = rp.json().get('respose').get('id')
                if restful_key_id :
                    res.write({'restful_key_id': restful_key_id})
            else :
                raise UserError((u'Restful接口连接失败错误'))            
        return  res

    @api.multi
    def write(self, vals):
        '''
            数据编辑时调用api
        :param vals:
        :return:
        '''
        #根据drivetype类型判断调用哪个表
        
        odoo_value = vals
        res = False
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        #批量更新
        for r in self:
            if r.drivetype == 'working' :
                TABLE = TABLE_work
            else :
                TABLE = TABLE_others                    
            
            seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
            if seconds.seconds < 5 or (odoo_value.get('state') in ('approved','moved')):
                res = super(DriveRecords, r).write(odoo_value)
            else:
                _logger.info('Start write data: %s', self._name)
                vals = mapping.dict_transfer(self._name, vals)
                vals.update({
                    'id': int(r.restful_key_id),
                    'line':r.route_id.line_name or '',
                    'selfId':r.vehicle_id.inner_code or '',
                    'onBoardId':int(r.vehicle_id.on_boardid),
                    'gprsId':r.route_id.gprs_id or '',
                    #'workerId':r.driver_id.jobnumber or '',
                    #'driver':r.driver_id.name or '',                    
                })
                if vals :
                    params = Params(type=3, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
                    #调用restful接口
                    rp = Client().http_post(url, data=params)
                    if rp:
                        if   rp.json().get('result') == 0 :
                            res = super(DriveRecords, r).write(odoo_value)
                        else :
                            raise UserError((u'更新错误.%s')%rp.json().get('respose').get('text'))
                    else:
                        raise UserError((u'接口连接失败错误'))                    
                                    
        return res

    @api.multi
    def unlink(self):
        '''
            数据删除时调用api
        :return:
        '''
        # fk_ids = self.mapped('fk_id')
        # vals = {"ids":fk_ids}
        # vals = {"ids": self.ids}
 
        
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        
        for r in self:
            if r.drivetype == 'working' :
                TABLE = TABLE_work
            else :
                TABLE = TABLE_others              
                     
            _logger.info('Start unlink data: %s', self._name)
            vals = {'id': int(r.restful_key_id)}
            
            res = super(DriveRecords, r).unlink()
            params = Params(type = 2, cityCode = cityCode,tableName = TABLE, data = vals).to_dict()
            #调用restful
            rp = Client().http_post(url, data=params)
            if rp :
                if  rp.json().get('result') != 0 :
                    raise UserError((u'删除错误.%s')%rp.json().get('respose').get('text'))   
            else :
                raise UserError((u'接口连接失败错误'))
            
        return