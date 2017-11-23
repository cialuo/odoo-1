# -*- coding: utf-8 -*-
from odoo import api, fields, models
import sms
class sendMessage(models.Model):

    _name = 'send_messages'
    _description = 'Send Messages'
    
    """
        发送消息
    """

    employee_id = fields.Many2one('hr.employee')  # 员工

    mobile = fields.Char(related='employee_id.mobile_phone', store=True, readonly=True)#手机号码

    sms_model_id = fields.Many2one('sms_model')#短信模板

    message_text = fields.Text(related='sms_model_id.message_text', store=True, readonly=True)

    tyep = fields.Selection([('sms','sms'),('weChat','weChat')])#发送类型

    message_status = fields.Selection([('2','success'),('403','failure')]) #状态

    @api.multi
    def create(self, vals):
        """
            创建一条消息，并且发送消息
        :param vals:
        :return:
        """

        if vals.has_key('tyep') and vals['tyep'] == sms:

            #短信发送
            if vals.has_key('mobile') and vals.has_key('sms_text'):
                r = sms().send_sms(vals['sms_text'],vals['mobile'])
                vals['message_status'] = r['code']
        else:
            #微信发送
            pass

        res = super(sendMessage, self).create(vals)
        return res



class smsModel(models.Model):

    _name = 'sms_model'
    _description = 'Sms Model'

    """
        发送短信的模板
    """

    name = fields.Char()#模板名称

    message_text = fields.Text()#消息主体

