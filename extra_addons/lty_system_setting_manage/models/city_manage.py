from odoo import api, fields, models

class lty_system_setting_city(models.Model):
    _name = "lty.system.setting.city"

    #城市名称
    name = fields.Char("城市名",required=True)
    #城市区号
    area_code = fields.Integer("区号")