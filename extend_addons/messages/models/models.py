# -*- coding: utf-8 -*-
from odoo import api, fields, models,_,exceptions
import httplib
import urllib
import re
class sendMessage(models.Model):

    _name = 'send_messages'
    _description = 'Send Messages'
    _rec_name = 'employee_id'
    """
        发送消息
    """

    employee_id = fields.Many2one('hr.employee',required=True)  # 员工

    mobile = fields.Char(related='employee_id.mobile_phone', store=True)#手机号码

    sms_model_id = fields.Many2one('sms_model',required=True)#短信模板

    message_text = fields.Text(related='sms_model_id.message_text', store=True)

    tyep = fields.Selection([('sms','sms'),('weChat','weChat')],default='sms')#发送类型

    message_status = fields.Selection([(2,'success'),(403,'failure'),(4072,'Format not reported')]) #状态

    @api.constrains('employee_id')
    def check_mobile(self):
        """
            检查手机
        :return:
        """
        for order in self:
            if not order.mobile:
                raise exceptions.ValidationError(_("Phone number does not exist!"))

    @api.constrains('sms_model_id')
    def check_message_text(self):
        """
            检查短信模板
        :return:
        """
        for order in self:
            if not order.message_text:
                raise exceptions.ValidationError(_("SMS template does not exist!"))

    @api.model
    def create(self, vals):
        """
            创建一条消息，并且发送消息
        :param vals:
        :return:
        """
        res = super(sendMessage, self).create(vals)

        if vals.has_key('tyep') and vals['tyep'] == 'sms':

            #短信发送
            if res.mobile and res.message_text:
                r = self.send_sms(res.message_text,res.mobile)
                text = eval(r)
                res.message_status = text['code']
        else:
            #微信发送
            pass

        return res


    def send_sms(self,text, mobile):

        host = "106.ihuyi.com"

        sms_send_uri = "/webservice/sms.php?method=Submit"
        # 用户名是登录
        account = "C40327916"
        # 密码
        password = "fbd368db490fd093e4d1ddd469abe0c9"
        params = urllib.urlencode({'account': account, 'password': password, 'content': text.encode('utf-8'), 'mobile': mobile, 'format': 'json'})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(host, port=80, timeout=30)
        conn.request("POST", sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        return response_str


class smsModel(models.Model):

    _name = 'sms_model'
    _description = 'Sms Model'

    """
        发送短信的模板
    """

    name = fields.Char()#模板名称

    message_text = fields.Text()#消息主体

