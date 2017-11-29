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

#对接系统  大站设置

TABLE = 'op_planstationbigmain'

_logger = logging.getLogger(__name__)
class Bigsitesetup(models.Model):

    _inherit = 'scheduleplan.bigsitesetup'

    '''
        继承大站设置数据,调用restful api
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

        res = super(Bigsitesetup, self).create(vals)

        if not self._context.get('dryrun'):
            url = self.env['ir.config_parameter'].get_param('restful.url')
            cityCode = self.env['ir.config_parameter'].get_param('city.code')

            rp = True
            try:
                _logger.info('Start create data: %s', self._name)
                if self._name == 'scheduleplan.bigsitesetup':
                    vals.update({
                        'id': str(res.id) + 'up',
                        'station_name': res.site_id.name,
                        'direction': 'up',
                        'line_id': res.rule_id.line_id.id,
                    })
                if self._name == 'scheduleplan.bigsitesetdown':
                    vals.update({
                        'id': str(res.id) + 'down',
                        'station_name': res.site_id.name,
                        'direction': 'down',
                        'line_id': res.rule_id.line_id.id,
                    })
                vals = mapping.dict_transfer(self._name, vals)
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

        res = super(Bigsitesetup, self).write(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
            if seconds.seconds > 5 and (not self._context.get('dryrun')):
                rp = True
                try:
                    # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                    _logger.info('Start write data: %s', self._name)
                    if self._name == 'scheduleplan.bigsitesetup':
                        vals.update({
                            'id': str(r.id) + 'up',
                            'station_name': r.site_id.name,
                            'direction': 'up',
                            'line_id': r.rule_id.line_id.id,
                        })
                    if self._name == 'scheduleplan.bigsitesetdown':
                        vals.update({
                            'id': str(r.id) + 'down',
                            'station_name': r.site_id.name,
                            'direction': 'down',
                            'line_id': r.rule_id.line_id.id,
                        })
                    vals = mapping.dict_transfer(self._name, vals)
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
        if self._name == 'scheduleplan.bigsitesetup':
            origin_ids += map(lambda x: str(x) + 'up', self.ids)
        if self._name == 'scheduleplan.bigsitesetdown':
            origin_ids += map(lambda x: str(x) + 'down', self.ids)
        # vals = {"ids": origin_ids}

        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for id in origin_ids:
            # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
            _logger.info('Start unlink data: %s', self._name)
            vals = {'id': id}
            params = Params(type = 2, cityCode = cityCode,tableName = TABLE, data = vals).to_dict()
            res = super(Bigsitesetup, r).unlink()
            rp = Client().http_post(url, data=params)
            response_check(rp)
        return
#
# class Bigsitesetdown(models.Model):
#
#     _inherit = 'scheduleplan.bigsitesetdown'
#
#     '''
#         继承大站设置数据,调用restful api
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
#         res = super(Bigsitesetdown, self).create(vals)
#         url = self.env['ir.config_parameter'].get_param('restful.url')
#         cityCode = self.env['ir.config_parameter'].get_param('city.code')
#         try:
#             _logger.info('Start create data: %s', self._name)
#
#
#             vals = mapping.dict_transfer(self._name, vals)
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
#         res = super(Bigsitesetdown, self).write(vals)
#         url = self.env['ir.config_parameter'].get_param('restful.url')
#         cityCode = self.env['ir.config_parameter'].get_param('city.code')
#         for r in self:
#             seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
#             if seconds.seconds > 5:
#                 try:
#                     # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
#                     _logger.info('Start write data: %s', self._name)
#                     vals.update({
#                         'id': str(r.id) + 'down',
#                         'station_name': r.site_id.name,
#                         'direction': 'down',
#                     })
#                     vals = mapping.dict_transfer(self._name, vals)
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
#         origin_ids = map(lambda x: str(x) + 'down', self.ids)
#         # vals = {"ids": origin_ids}
#         res = super(Bigsitesetdown, self).unlink()
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