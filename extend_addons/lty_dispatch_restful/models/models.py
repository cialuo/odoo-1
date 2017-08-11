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
        try:
            url = 'http://10.1.50.83:8080/ltyop/syn/synData/'
            params = Params(type = 1, cityCode = 'SZ',tableName = 'op_line', data = vals).to_dict()
            id = Client().http_post(url,data=params)
            if id:
                vals['fk_id'] = id
        except Exception,e:
            print e
        return super(op_line, self).create(vals)

    @api.multi
    def write(self, vals):
        '''
            数据编辑时调用api
        :param vals:
        :return:
        '''
        res = super(op_line, self).write(vals)
        if res:
            #Client('op_line', 3, vals).push()
            pass
        return res

    @api.multi
    def unlink(self):
        '''
            数据删除时调用api
        :return:
        '''
        self.fk_id
        res = super(op_line, self).unlink()
        if res:
            #client('op_line', 2, vals).push()
            pass
        return res

    def to_bean(self,vals):
        '''
            把数据装换为
        :return:
        '''