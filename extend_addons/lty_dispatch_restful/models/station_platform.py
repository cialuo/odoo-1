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
import logging
import time

#对接系统  站点基础数据表名

TABLE = 'op_station'

_logger = logging.getLogger(__name__)
class Station(models.Model):

    _inherit = 'opertation_resources_station_platform'

    '''
        继承站点基础数据,调用restful api
    '''

    # #调度数据逐渐
    # fk_id = fields.Char()

    @api.model
    def create(self, vals):
        '''
            数据创建完成调用api
        :param vals:
        :return:
        '''

        res = super(Station, self).create(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        try:
            _logger.info('Start create data: %s', self._name)
            vals = mapping.dict_transfer(self._name, vals)
            vals.update({
                'id': res.id,
                'gprsId': res.route_id.gprs_id,
                'stationName': res.station_id.name,
                'longitude': res.station_id.entrance_longitude,
                'latitude': res.station_id.entrance_latitude,
                'angle': res.station_id.entrance_azimuth,
                'longitudeOut': res.station_id.exit_longitude,
                'latitudeOut': res.station_id.exit_latitude,
                'angleOut': res.station_id.exit_azimuth,
            })
            params = Params(type=1, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
            rp = Client().http_post(url, data=params)
        except Exception,e:
            _logger.info('%s', e.message)
        return res

    @api.multi
    def write(self, vals):
        '''
            数据编辑时调用api
        :param vals:
        :return:
        '''

        res = super(Station, self).write(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            #时间戳 避免 create方法进入 write方法
            seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
            if seconds.seconds > 5:
                try:
                    # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                    _logger.info('Start write data: %s', self._name)
                    vals = mapping.dict_transfer(self._name, vals)
                    vals.update({
                        'id': r.id,
                        'gprsId': r.route_id.gprs_id,
                        'stationName': r.station_id.name,
                        'longitude': r.station_id.entrance_longitude,
                        'latitude': r.station_id.entrance_latitude,
                        'angle': r.station_id.entrance_azimuth,
                        'longitudeOut': r.station_id.exit_longitude,
                        'latitudeOut': r.station_id.exit_latitude,
                        'angleOut': r.station_id.exit_azimuth,
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
        res = super(Station, self).unlink()
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            try:
                # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                _logger.info('Start unlink data: %s', self._name)
                vals = {'id': r.id}
                params = Params(type = 2, cityCode = cityCode,tableName = TABLE, data = vals).to_dict()
                rp = Client().http_post(url, data=params)
            except Exception,e:
                _logger.info('%s', e.message)
        return res