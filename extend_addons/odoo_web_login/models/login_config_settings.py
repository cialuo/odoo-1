# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class LoginConfigSettings(models.TransientModel):
    _name = 'login_config_settings'
    _inherit = 'res.config.settings'

    @api.model
    def default_get(self, fields):
        res = super(LoginConfigSettings, self).default_get(fields)
        val=self.env['login_config_settings'].search([], limit=1, order="id desc")
        if val:
            res['banner_img_src'] = val.banner_img_src
            res['background_img_src'] = val.background_img_src
            res['login_img_src'] = val.login_img_src
            res['banner_img_offset_src'] = val.banner_img_offset_src
            res['login_dialog_offset_src'] = val.login_dialog_offset_src
            res['header_height_src'] = val.header_height_src
            res['footer_height_src'] = val.footer_height_src
            res['body_login_height_src'] = val.body_login_height_src
        return res

    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    banner_img_src = fields.Char(string="Banner Img Src", default="/odoo_web_login/static/src/img/banner_img.png", readonly="True")

    background_img_src = fields.Char(string="Background Img Src", default="/odoo_web_login/static/src/img/background_img.png", readonly="True")

    login_img_src = fields.Char(string="Login Img Src", default="/odoo_web_login/static/src/img/login_img.png", readonly="True")

    banner_img_offset_src = fields.Selection([
        ('col-md-offset-0', '0'),
        ('col-md-offset-1', '1'),
        ('col-md-offset-2', '2'),
        ('col-md-offset-3', '3'),
        ('col-md-offset-4', '4'),
        ('col-md-offset-5', '5'),
        ('col-md-offset-6', '6'),
        ('col-md-offset-7', '7'),
        ('col-md-offset-8', '8'),
        ('col-md-offset-9', '9'),
        ('col-md-offset-10', '10')
        ], string="Banner Img Offset Src", default='col-md-offset-0')

    login_dialog_offset_src = fields.Selection([
        ('col-md-offset-0', '0'),
        ('col-md-offset-1', '1'),
        ('col-md-offset-2', '2'),
        ('col-md-offset-3', '3'),
        ('col-md-offset-4', '4'),
        ('col-md-offset-5', '5'),
        ('col-md-offset-6', '6'),
        ('col-md-offset-7', '7'),
        ('col-md-offset-8', '8'),
        ('col-md-offset-9', '9')
        ], string="Login Dialog Offset Src", default='col-md-offset-7')

    header_height_src = fields.Integer(string="Header Height Src", default="5")

    footer_height_src = fields.Integer(string="Footer Height Src", default="20")

    body_login_height_src = fields.Integer(string="Body Login Height Src", default="75")

    @api.model
    def create(self, vals):
        result = super(LoginConfigSettings, self).create(vals)
        height=result.header_height_src+result.footer_height_src+result.body_login_height_src
        if height != 100:
            raise exceptions.ValidationError(_('The height value may not be incorrect'))
        return result
