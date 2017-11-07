from odoo import models, fields, api

class lty_role(models.Model):
    _name = "lty.role"

    #角色名称
    name = fields.Char()
    #人员ID
    user_id = fields.Many2one("lty.user.information")