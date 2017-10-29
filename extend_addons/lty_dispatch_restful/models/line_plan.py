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

#对接系统  线路计划基础数据表名

LINEPLAN_TABLE = 'op_linePlan'

_logger = logging.getLogger(__name__)
class LinePlan(models.Model):

    _inherit = 'scheduleplan.schedulrule'

    '''
        继承人员基础数据,调用restful api
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

        res = super(LinePlan, self).create(vals)
        if not self._context.get('dryrun'):
            url = self.env['ir.config_parameter'].get_param('restful.url')
            cityCode = self.env['ir.config_parameter'].get_param('city.code')
            rp = True
            try:
                _logger.info('Start create data: %s', self._name)
                vals.update({
                    'id': res.id,
                    #后台取值,
                    'gprs_id': res.line_id.gprs_id,
                    'schedule_type': res.line_id.schedule_type,
                    'line_id': res.line_id.id,
                    'upfirsttime': '2017-01-01 ' + res.upfirsttime + ':00',
                    'uplasttime': '2017-01-01 ' + res.uplasttime + ':00',
                    'downfirsttime': '2017-01-01 ' + res.downfirsttime + ':00',
                    'downlasttime': '2017-01-01 ' + res.downlasttime + ':00',
                    # 'upfirsttime': res.upfirsttime,
                    # 'uplasttime': res.uplasttime,
                    # 'downfirsttime': res.downfirsttime,
                    # 'downlasttime': res.downlasttime,
                })
                vals = mapping.dict_transfer(self._name, vals)
                params = Params(type=1, cityCode=cityCode,tableName=LINEPLAN_TABLE, data=vals).to_dict()
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

        res = super(LinePlan, self).write(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
            if seconds.seconds > 5 and (not self._context.get('dryrun')):
                rp = True
                try:
                    # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                    _logger.info('Start write data: %s', self._name)
                    vals.update({
                        'id': r.id,
                        'line_id': r.line_id.id,
                        'upfirsttime': '2017-01-01 ' + r.upfirsttime + ':00',
                        'uplasttime': '2017-01-01 ' + r.uplasttime + ':00',
                        'downfirsttime': '2017-01-01 ' + r.downfirsttime + ':00',
                        'downlasttime': '2017-01-01 ' + r.downlasttime + ':00',
                        # 后台取值,
                        'gprs_id': r.line_id.gprs_id,
                        'schedule_type': r.line_id.schedule_type,
                    })
                    vals = mapping.dict_transfer(self._name, vals)
                    params = Params(type=3, cityCode=cityCode,tableName=LINEPLAN_TABLE, data=vals).to_dict()
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
        # vals = {"ids": self.ids}

        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
            vals = {'id': r.id}
            _logger.info('Start unlink data: %s', self._name)
            params = Params(type = 2, cityCode = cityCode,tableName = LINEPLAN_TABLE, data = vals).to_dict()
            res = super(LinePlan, r).unlink()
            rp = Client().http_post(url, data=params)
            response_check(rp)

            r.bigsite_up.unlink()
            r.bigsite_down.unlink()
            r.uptimearrange.unlink()
            r.downtimearrange.unlink()

        return res