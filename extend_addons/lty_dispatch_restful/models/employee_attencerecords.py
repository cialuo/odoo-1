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
import logging

#对接系统  考勤信息表

TABLE = 'attend'

_logger = logging.getLogger(__name__)
class attence(models.Model):

    _inherit = 'employee.attencerecords'

    '''
        继承考勤记录,调用restful api
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

        res = super(attence, self).create(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        if vals.get('is_add'):
            try:
                _logger.info('Start create data: %s', self._name)
                vals = mapping.dict_transfer(self._name, vals)
                vals.update({
                    'onboardId': int(res.vehicle_id.on_boardid),
                    'selfId': res.vehicle_id.inner_code,
                    'gprsId': res.line_id.gprs_id,
                    'workerId': res.employee_id.jobnumber,
                    'driver': res.employee_id.name,
                    'WorkerType': int(res.work_type_id),                    
                })
                params = Params(type=1, cityCode=cityCode, tableName=TABLE, data=vals).to_dict()
                rp = Client().http_post(url, data=params)
                restful_key_id = rp.json().get('respose').get('id')
                rp.text
                if restful_key_id :
                    res.write({'restful_key_id': int(restful_key_id)})
                else :
                    raise UserError((u'插入错误.'))            
            except Exception, e:
                _logger.info('%s', e.message)
        return res

    @api.multi
    def write(self, vals):
        '''
            数据编辑时调用api
        :param vals:
        :return:
        '''

        res = super(attence, self).write(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            if r.id != 1:
                seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
                if seconds.seconds > 5:
                    try:
                        # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                        _logger.info('Start write data: %s', self._name)
                        vals = mapping.dict_transfer(self._name, vals)
                        if vals:
                            vals.update({
                                'id': int(r.restful_key_id),
                                'WorkerType': r.work_type_id,                    
                            })
                            params = Params(type=3, cityCode=cityCode,tableName=TABLE, data=vals).to_dict()
                            rp = Client().http_post(url, data=params)
                            rp.text

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
            r.work_type_id
            try:
                # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                _logger.info('Start unlink data: %s', self._name)
                vals = {'id': int(r.restful_key_id),'WorkerType': r.work_type_id}
                res = super(attence, r).unlink()
                params = Params(type = 2, cityCode = cityCode,tableName = TABLE, data = vals).to_dict()
                rp = Client().http_post(url, data=params)
                rp.text
            except Exception,e:
                _logger.info('%s', e.message)
        return res