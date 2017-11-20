from odoo import models, fields, api

#人员信息模块
class lty_user_information(models.Model):
    _name = "lty.user.information"

    #姓名
    name = fields.Char()
    #用户名
    user_name = fields.Char()
    #所属彻城市
    belong_city = fields.Many2one("lty.system.setting.city")
    #所属公司
    belong_company = fields.Many2one("lty.bus.company.manage")
    #密码
    pass_word = fields.Char()
    #角色
    role = fields.One2many("lty.role","user_id","user_id")