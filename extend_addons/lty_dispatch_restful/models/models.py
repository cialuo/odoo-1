# -*- coding: utf-8 -*-

from odoo import models, fields, api
from extend_addons.lty_dispatch_restful.core.restful_client import *

class op_line(models.Model):

    _inherit = 'route_manage.route_manage'

    '''
        继承线路模块,在线路数据创建时,调用restful api
    '''

    #调度数据逐渐
    fk_id = fields.Char()

    @api.model
    def create(self, vals):
        '''
            数据创建完成调用api
        :param vals:
        :return:
        '''

        for p in self:
            print not isinstance(p.id,models.NewId)

        vals['restful_type'] = 1
        res = super(op_line, self).create(vals)
        try:
            url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
            params = Params(type = 1, cityCode = 'SZ',tableName = 'op_line', data = vals).to_dict()
            rp = Client().http_post(url, data=params)
            #clientThread(url,params,res).start()
        except Exception,e:
            print e.message
        return res

    @api.multi
    def write(self, vals):
        '''
            数据编辑时调用api
        :param vals:
        :return:
        '''
        for p in self:
            print not isinstance(p.id,models.NewId)


        res = super(op_line, self).write(vals)
        if vals.get('restful_type') != 1:
            try:
                url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
                params = Params(type = 3, cityCode = 'SZ',tableName = 'op_line', data = vals).to_dict()
                clientThread(url,params,res).start()
            except Exception,e:
                print e.message
        return res

    @api.multi
    def unlink(self):
        '''
            数据删除时调用api
        :return:
        '''
        fk_ids = self.mapped('fk_id')
        vals = {"ids":fk_ids}
        res = super(op_line, self).unlink()
        try:
            url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
            params = Params(type = 3, cityCode = 'SZ',tableName = 'op_line', data = vals).to_dict()
            clientThread(url,params,res).start()
        except Exception,e:
            print e.message
        return res

    def to_bean(self,vals):
        '''
            把数据装换为
        :return:
        '''