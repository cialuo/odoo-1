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

        res = super(DriveRecords, self).create(vals)
        vals_odoo = vals
        if vals.get('drivetype') == 'working' :
            TABLE = TABLE_work
        else :
            TABLE = TABLE_others
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        if  vals.get('is_add') :
            try:
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
                rp = Client().http_post(url, data=params)
                restful_key_id = rp.json().get('respose').get('id')
                if restful_key_id :
                    res.write({'restful_key_id': restful_key_id})
            except Exception,e:
                _logger.info('%s', e.message)
        return  res

    @api.multi
    def write(self, vals):
        '''
            数据编辑时调用api
        :param vals:
        :return:
        '''

        res = super(DriveRecords, self).write(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            if vals.get('drivetype') == 'working' :
                TABLE = TABLE_work
            else :
                TABLE = TABLE_others
            if r.id != -1:
                seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
                if seconds.seconds > 5:
                    try:
                        # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                        _logger.info('Start write data: %s', self._name)
                        vals = mapping.dict_transfer(self._name, vals)
                        if vals:
                            vals.update({
                                'id': int(r.restful_key_id),
                            })
                            params = Params(type=3, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
                            rp = Client().http_post(url, data=params)

                        # clientThread(url,params,res).start()
                    except Exception,e:
                        _logger.info('%s', e.message)
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
            try:
                # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                _logger.info('Start unlink data: %s', self._name)
                vals = {'id': int(r.restful_key_id)}
                
                res = super(DriveRecords, r).unlink()
                params = Params(type = 2, cityCode = cityCode,tableName = TABLE, data = vals).to_dict()
                rp = Client().http_post(url, data=params)
            except Exception,e:
                _logger.info('%s', e.message)
        return res