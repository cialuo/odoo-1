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

#对接系统  调度计划

TABLE = 'op_dispatchplan'

_logger = logging.getLogger(__name__)
class upplanitem(models.Model):

    _inherit = 'scheduleplan.execupplanitem'

    '''
        继承排班计划,调用restful api
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

        res = super(upplanitem, self).create(vals)
        if not self._context.get('dryrun'):
            url = self.env['ir.config_parameter'].get_param('restful.url')
            cityCode = self.env['ir.config_parameter'].get_param('city.code')

            rp = True
            if res.execplan_id.rule_id.schedule_method == 'dubleway':
                plan_count = 0.5
            if res.execplan_id.rule_id.schedule_method == 'singleway':
                plan_count = 1                
            try:
                _logger.info('Start create data: %s', self._name)
                vals = mapping.dict_transfer(self._name, vals)
                vals.update({
                    'lineName': res.execplan_id.line_id.line_name,
                    'gprsId': res.execplan_id.line_id.gprs_id,
                    'selfId': res.vehicle_id.inner_code,
                    'onBoardId': res.vehicle_id.on_boardid,
                    'workerId': res.driver.jobnumber,
                    'driverName': res.driver.name,
                    'trainName': res.steward.name,
                    'trainId': res.steward.jobnumber,
                    'workDate': res.execplan_id.excutedate,
                    'lineId': res.execplan_id.line_id.id,
                    'runGprsId': res.line_id.gprs_id,
                    'linePlanId': res.execplan_id.rule_id.id,
                })
                if self._name == 'scheduleplan.execupplanitem':
                    vals.update({
                        'id': int(str(res.id) + '0'),
                        'direction': 0,
                        'planCount': plan_count,
                    })
                if self._name == 'scheduleplan.execdownplanitem':
                    vals.update({
                        'id': int(str(res.id) + '1'),
                        'direction': 1,
                        'planCount': plan_count,
                    })
                params = Params(type=1, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
                rp = Client().http_post(url, data=params)

            except Exception,e:
                _logger.info('%s', e.message)

            response_check(rp)
        return res

    @api.multi
    def write(self, vals):
        '''
            数据编辑时调用api
        :param vals:
        :return:
        '''

        res = super(upplanitem, self).write(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
            if seconds.seconds > 5 and (not self._context.get('dryrun')):
                rp = True
                try:
                    # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                    _logger.info('Start write data: %s', self._name)
                    vals = mapping.dict_transfer(self._name, vals)
                    vals.update({
                        # 'id': int(str(r.id) + '0'),
                        'lineName': r.execplan_id.line_id.line_name,
                        'gprsId': r.execplan_id.line_id.gprs_id,
                        'selfId': r.vehicle_id.inner_code,
                        'onBoardId': r.vehicle_id.on_boardid,
                        'workerId': r.driver.jobnumber,
                        'driverName': r.driver.name,
                        'trainName': r.steward.name,
                        'trainId': r.steward.jobnumber,
                        'workDate': r.execplan_id.excutedate,
                        'lineId': r.execplan_id.line_id.id,
                        'runGprsId': r.line_id.gprs_id,
                        'linePlanId': r.execplan_id.rule_id.id,

                        # 'direction': 0,
                    })
                    if self._name == 'scheduleplan.execupplanitem':
                        vals.update({
                            'id': int(str(r.id) + '0'),
                            'direction': 0,
                        })
                    if self._name == 'scheduleplan.execdownplanitem':
                        vals.update({
                            'id': int(str(r.id) + '1'),
                            'direction': 1,
                        })
                    params = Params(type=3, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
                    rp = Client().http_post(url, data=params)

                    # clientThread(url,params,res).start()
                except Exception,e:
                    _logger.info('%s', e.message)

                response_check(rp)
        return res

    @api.multi
    def unlink(self):
        '''
            数据删除时调用api
        :return:
        '''
        # fk_ids = self.mapped('fk_id')
        # vals = {"ids":fk_ids}
        origin_ids = []
        if self._name == 'scheduleplan.execupplanitem':
            origin_ids += map(lambda x: int(str(x) + '0'), self.ids)
        if self._name == 'scheduleplan.execdownplanitem':
            origin_ids += map(lambda x: int(str(x) + '1'), self.ids)
        # vals = {"ids": origin_ids}
        res = super(upplanitem, self).unlink()
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for up_id in origin_ids:
            try:
                # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                _logger.info('Start unlink data: %s', self._name)
                vals = {'id': up_id}
                params = Params(type = 2, cityCode = cityCode,tableName = TABLE, data = vals).to_dict()
                rp = Client().http_post(url, data=params)
            except Exception,e:
                _logger.info('%s', e.message)
            response_check(rp)
        return res

#整条执行表删除,删除对应的司成，车辆资源。调度计划
class Excutetable(models.Model):
    _inherit = 'scheduleplan.excutetable'

    @api.multi
    def unlink(self):
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for s in self:
            # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
            _logger.info('Start unlink data: %s', self._name)
            vals = {'lineId': s.line_id.id, 'workDate': s.excutedate}
            params = Params(type = 2, cityCode = cityCode,tableName='op_dispatchplan', data = vals).to_dict()
            res = super(Excutetable, s).unlink()
            rp = Client().http_post(url, data=params)
            response_check(rp)
        return res

# class downplanitem(models.Model):
#
#     _inherit = 'scheduleplan.execdownplanitem'
#
#     '''
#         继承排班计划,调用restful api
#     '''
#
#     # #调度数据逐渐
#     # fk_id = fields.Char()
#
#     @api.model
#     def create(self, vals):
#         '''
#             数据创建完成调用api
#         :param vals:
#         :return:
#         '''
#
#         res = super(downplanitem, self).create(vals)
#         url = self.env['ir.config_parameter'].get_param('restful.url')
#         cityCode = self.env['ir.config_parameter'].get_param('city.code')
#         try:
#             _logger.info('Start create data: %s', self._name)
#             vals = mapping.dict_transfer(self._name, vals)
#             vals.update({
#                 'id': int(str(res.id)+'1'),
#                 'lineName': res.line_id.line_name,
#                 'gprsId': res.line_id.gprs_id,
#                 'selfId': res.vehicle_id.inner_code,
#                 'onBoardId': res.vehicle_id.on_board_id,
#                 'workerId': res.driver.jobnumber,
#                 'direction': 0,
#             })
#             params = Params(type=1, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
#             rp = Client().http_post(url, data=params)
#         except Exception,e:
#             _logger.info('%s', e.message)
#         return res
#
#     @api.multi
#     def write(self, vals):
#         '''
#             数据编辑时调用api
#         :param vals:
#         :return:
#         '''
#
#         res = super(downplanitem, self).write(vals)
#         url = self.env['ir.config_parameter'].get_param('restful.url')
#         cityCode = self.env['ir.config_parameter'].get_param('city.code')
#         for r in self:
#             seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
#             if seconds.seconds > 5:
#                 try:
#                     # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
#                     _logger.info('Start write data: %s', self._name)
#                     vals = mapping.dict_transfer(self._name, vals)
#                     vals.update({
#                         'id': int(str(r.id) + '1'),
#                         'lineName': r.line_id.line_name,
#                         'gprsId': r.line_id.gprs_id,
#                         'selfId': r.vehicle_id.inner_code,
#                         'onBoardId': r.vehicle_id.on_board_id,
#                         'workerId': r.driver.jobnumber,
#                         'direction': 0,
#                     })
#                     params = Params(type=3, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
#                     rp = Client().http_post(url, data=params)
#
#                     # clientThread(url,params,res).start()
#                 except Exception,e:
#                     _logger.info('%s', e.message)
#         return res
#
#     @api.multi
#     def unlink(self):
#         '''
#             数据删除时调用api
#         :return:
#         '''
#         # fk_ids = self.mapped('fk_id')
#         # vals = {"ids":fk_ids}
#         origin_ids = map(lambda x: int(str(x) + '1'), self.ids)
#         # vals = {"ids": origin_ids}
#         res = super(downplanitem, self).unlink()
#         url = self.env['ir.config_parameter'].get_param('restful.url')
#         cityCode = self.env['ir.config_parameter'].get_param('city.code')
#         for down_id in origin_ids:
#             try:
#                 # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
#                 _logger.info('Start unlink data: %s', self._name)
#                 vals = {'id': down_id}
#                 params = Params(type = 2, cityCode = cityCode,tableName = TABLE, data = vals).to_dict()
#                 rp = Client().http_post(url, data=params)
#             except Exception,e:
#                 _logger.info('%s', e.message)
#         return res