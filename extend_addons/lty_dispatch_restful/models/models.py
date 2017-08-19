# -*- coding: utf-8 -*-

from odoo import models, fields, api
from extend_addons.lty_dispatch_restful.core.restful_client import *
import mapping
import logging

#对接系统
#线路基础数据表名
LINE_TABLE = 'op_line'
#站台基础数据表名
STATION_TABLE = 'op_stationblock'

_logger = logging.getLogger(__name__)

class op_line(models.Model):

    _inherit = 'route_manage.route_manage'

    '''
        继承线路模块,在线路数据创建时,调用restful api
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
        res = super(op_line, self).create(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        try:
            # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
            _logger.info('Start create data: %s', self._name)
            vals = mapping.dict_transfer(self._name, vals)
            vals.update({
                'id': res.id,
                #增加默认传值
                'isRoundLine': 0,
                'isNight': 0,
                'isCrossDay': 0,
                'isShowPoint': 0,
                'isShowStationName': 0,
            })
            params = Params(type=1, cityCode=cityCode,tableName=LINE_TABLE, data=vals).to_dict()
            rp = Client().http_post(url, data=params)

            #clientThread(url,params,res).start()
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
        res = super(op_line, self).write(vals)
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        for r in self:
            second_create = int(r.create_date[-2:])
            second_now = int(fields.Datetime.now()[-2:])
            if second_now - second_create > 5:
                try:
                    # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                    _logger.info('Start write data: %s', self._name)
                    vals = mapping.dict_transfer(self._name, vals)
                    vals.update({'id': r.id})
                    params = Params(type=3, cityCode=cityCode, tableName=LINE_TABLE, data=vals).to_dict()
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
            try:
                # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                _logger.info('Start unlink data: %s', self._name)
                vals = {'id': r.id}
                params = Params(type=2, cityCode=cityCode, tableName=LINE_TABLE, data=vals).to_dict()
                rp = Client().http_post(url, data=params)
                # clientThread(url,params,res).start()
            except Exception,e:
                _logger.info('%s', e.message)
        res = super(op_line, self).unlink()
        return res

class Station(models.Model):
    _inherit = 'opertation_resources_station'
    """
     继承站台模块,在站台数据创建时,调用restful api
    """
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
            })
            params = Params(type=1, cityCode=cityCode,tableName=STATION_TABLE, data=vals).to_dict()
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
            second_create = int(r.create_date[-2:])
            second_now = int(fields.Datetime.now()[-2:])
            if second_now - second_create > 5:
                try:
                    _logger.info('Start write data: %s', self._name)
                    vals = mapping.dict_transfer(self._name, vals)
                    vals.update({'id': r.id})
                    params = Params(type=3, cityCode=cityCode,tableName=STATION_TABLE, data=vals).to_dict()
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
        vals = {"ids": self.ids}
        res = super(Station, self).unlink()
        url = self.env['ir.config_parameter'].get_param('restful.url')
        cityCode = self.env['ir.config_parameter'].get_param('city.code')
        try:
            _logger.info('Start unlink data: %s', self._name)
            params = Params(type=3, cityCode=cityCode,tableName=STATION_TABLE, data=vals).to_dict()
            clientThread(url,params,res).start()
        except Exception,e:
            _logger.info('%s', e.message)
        return res