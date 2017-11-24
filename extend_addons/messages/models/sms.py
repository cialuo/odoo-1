# -*- coding: utf-8 -*-
import httplib
import urllib
import json
host  = "106.ihuyi.com"

sms_send_uri = "/webservice/sms.php?method=Submit"

#用户名是登录
account  = "C40327916"
#密码
password = "fbd368db490fd093e4d1ddd469abe0c9"

class sms(object):

    def send_sms(self,text, mobile):
        params = urllib.urlencode(
            {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(host, port=80, timeout=30)
        conn.request("POST", sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        encode_json = json.dumps(response_str)
        return json.loads(encode_json)

if __name__ == '__main__':
    mobile = "18617121307"
    text = "您的验证码是：121254。请不要把验证码泄露给其他人。"
    s = sms()
    print(s.send_sms(text,mobile))

    #str = {"code": 2, "msg": "\u63d0\u4ea4\u6210\u529f", "smsid": "15113324934296638191"}


