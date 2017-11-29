from odoo import models, fields, api

class lty_bus_company_manage(models.Model):
    _name = "lty.bus.company.manage"

    #公司名称
    name = fields.Char()
    #所属城市
    belong_city = fields.Many2one("lty.system.setting.city")
    #总人数
    head_count = fields.Integer()