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

#对接系统
#出勤司机
#出勤乘务员


_logger = logging.getLogger(__name__)
class attendance(models.Model):

    _inherit = 'scheduleplan.motorcyclists'

    '''
        继承出勤司乘,调用restful api
    '''

    #调度数据逐渐
    # fk_id = fields.Char()

    @api.model
    def create(self, vals):
        '''
            数据创建完成调用api
        :param vals:
        :return:
        '''

        res = super(attendance, self).create(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        try:
            _logger.info('Start create data: %s', self._name)
            table = self._name + '.%s' % res.title
            vals = mapping.dict_transfer(table, vals)
            vals.update({
                'id': res.id,
                'lineId': res.execplan_id.line_id.id,
                'lineName': res.execplan_id.line_id.line_name,
                'gprsId': res.execplan_id.line_id.gprs_id,
                'selfId': res.vehicle_id.inner_code,
                'onBoardId': res.vehicle_id.on_boardid,
            })
            if res.title == 'driver':
                # 出勤司机
                TABLE = 'op_attendance'
                vals.update({'driverName': res.employee_id.name})
            if res.title == 'steward':
                # 出勤乘务员
                TABLE = 'op_trainattendance'
                vals.update({'trainName': res.employee_id.name})
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

        res = super(attendance, self).write(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
            if seconds.seconds > 5:
                try:
                    # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                    _logger.info('Start write data: %s', self._name)
                    table = self._name + '.%s' % r.title
                    vals = mapping.dict_transfer(table, vals)
                    vals.update({
                        'id': r.id,
                        'lineId': r.execplan_id.line_id.id,
                        'lineName': r.execplan_id.line_id.line_name,
                        'gprsId': r.execplan_id.line_id.gprs_id,
                        'selfId': r.vehicle_id.inner_code,
                        'onBoardId': r.vehicle_id.on_boardid,
                    })
                    if r.title == 'driver':
                        # 出勤司机
                        TABLE = 'op_attendance'
                        vals.update({'driverName': r.employee_id.name})
                    if r.title == 'steward':
                        # 出勤乘务员
                        TABLE = 'op_trainattendance'
                        vals.update({'trainName': r.employee_id.name})
                    params = Params(type=3, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
                    rp = Client().http_post(url, data=params)
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
        drivervals = self.filtered(lambda x: x.title == 'driver').ids
        stewardvals = self.filtered(lambda x: x.title == 'steward').ids
        res = super(attendance, self).unlink()
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        try:
            # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
            _logger.info('Start unlink data: %s', self._name)
            #出勤司机
            if drivervals:
                for driver in drivervals:
                    params = Params(type = 2, cityCode = cityCode,tableName = 'op_attendance', data = {'id': driver}).to_dict()
                    rp = Client().http_post(url, data=params)
            #出勤乘务员
            if stewardvals:
                for steward in stewardvals:
                    params = Params(type = 2, cityCode = cityCode,tableName = 'op_trainattendance', data = {'id': steward}).to_dict()
                    rp = Client().http_post(url, data=params)
        except Exception,e:
            _logger.info('%s', e.message)
        return res
