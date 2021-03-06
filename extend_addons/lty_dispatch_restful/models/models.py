# -*- coding: utf-8 -*-

from odoo import models, fields, api
from extend_addons.lty_dispatch_restful.core.restful_client import *
from odoo.exceptions import RedirectWarning, UserError, ValidationError
import mapping
import logging
import time

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
        
        if not self._context.get('dryrun'):
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
            if not res.start_date and vals.get('startDate'):
                del vals['startDate']
            if not res.end_date and  vals.get('endDate'):
                del vals['endDate']
            params = Params(type=1, cityCode=cityCode,tableName=LINE_TABLE, data=vals).to_dict()
            rp = Client().http_post(url, data=params)
            #clientThread(url,params,res).start()
            if rp:
                if rp.json().get('result') != 0 :
                    raise UserError((u'后台增加数据错误.%s')%rp.json().get('respose').get('text'))            
            else :
                raise UserError((u'Restful接口连接失败错误'))              
            
            
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
            #时间戳 避免 create方法进入 write方法
            # create_time = time.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")
            # time_create = int(time.mktime(create_time))
            # time_now = time.time()
            seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(r.create_date, "%Y-%m-%d %H:%M:%S")

            if seconds.seconds > 5 and (not self._context.get('dryrun')):
                rp = True
                try:
                    # url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                    _logger.info('Start write data: %s', self._name)
                    vals = mapping.dict_transfer(self._name, vals)
                    if vals:
                        vals.update({'id': r.id})
                        if not r.start_date and vals.get('startDate'):
                            del vals['startDate']
                        if not r.end_date and vals.get('endDate'):
                            del vals['endDate']
                        params = Params(type=3, cityCode=cityCode, tableName=LINE_TABLE, data=vals).to_dict()
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
            _logger.info('Start unlink data: %s', self._name)
            vals = {'id': r.id}
            res = super(op_line, r).unlink()
            params = Params(type=2, cityCode=cityCode, tableName=LINE_TABLE, data=vals).to_dict()
            rp = Client().http_post(url, data=params)
            response_check(rp)
            # clientThread(url,params,res).start()
        return

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
        if not self._context.get('dryrun'):
            rp = True
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
            response_check(rp)
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
            if seconds.seconds > 5 and (not self._context.get('dryrun')):
                rp = True
                try:
                    _logger.info('Start write data: %s', self._name)
                    vals = mapping.dict_transfer(self._name, vals)
                    if vals:
                        vals.update({'id': r.id})
                        params = Params(type=3, cityCode=cityCode,tableName=STATION_TABLE, data=vals).to_dict()
                        rp = Client().http_post(url, data=params)
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
            vals = {'id': r.id}
            _logger.info('Start unlink data: %s', self._name)
            params = Params(type=2, cityCode=cityCode,tableName=STATION_TABLE, data=vals).to_dict()
            res = super(Station, r).unlink()
            rp = Client().http_post(url, data=params)
            response_check(rp)

        return