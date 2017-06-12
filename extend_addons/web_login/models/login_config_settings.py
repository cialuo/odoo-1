# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _, models, modules, tools
from odoo.exceptions import ValidationError

class LoginConfigSettings(models.Model):
    _name = 'login_config_settings'

    name = fields.Char(string="Style Name", required=True) # 名称

    # banner_img_src = fields.Binary(string="Banner Img Src", readonly="true")


    def _default_image_background(self):
        context = dict(self._context or {})
        image_path = modules.get_module_resource('web_login', 'static/src/img', 'background_img.jpg')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    background_img_src = fields.Binary(string="Background Img Src", required=True, default=_default_image_background)

    def _default_image_login(self):
        context = dict(self._context or {})
        print context
        image_path = modules.get_module_resource('web_login', 'static/src/img', 'login_img.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    login_img_src = fields.Binary(string="Login Img Src", required=True, default=_default_image_login)

    header_height_src = fields.Integer(string="Header Height Src", default="10", required=True)

    footer_height_src = fields.Integer(string="Footer Height Src", default="15", required=True)

    body_login_height_src = fields.Integer(string="Body Login Height Src", default="75", required=True)

    state = fields.Selection([
        ('using', 'Using'),
        ('inactive', 'Inactive'),
        ], string="Custom State", default='inactive')

    def action_using(self):
        vals=self.search([('state', '=', 'using')])
        vals.write({'state':'inactive'})
        self.state = 'using'

    @api.multi
    def action_inactive(self):
        self.state = 'inactive'

    # @api.constrains('body_login_height_src')
    # def _check_body_login_height_src(self):
    #     for record in self:
    #         if record.body_login_height_src < 60:
    #             raise ValidationError(_('The body height value must not less than 60'))


    @api.constrains('header_height_src','footer_height_src','body_login_height_src')
    def _check_body_login_height_src(self):
        for record in self:
            if record.body_login_height_src < 60:
                raise ValidationError(_('The body height value must not less than 60'))
            if record.header_height_src>=0 and record.footer_height_src>=0 and record.body_login_height_src>=0:
                height = record.header_height_src + record.footer_height_src + record.body_login_height_src
                if height != 100:
                    raise exceptions.ValidationError(_('The height value may not be incorrect'))



    @api.model
    def create(self, vals):
        result = super(LoginConfigSettings, self).create(vals)
        height=result.header_height_src+result.footer_height_src+result.body_login_height_src
        if height != 100:
            raise exceptions.ValidationError(_('The height value may not be incorrect'))
        return result



    # @api.multi
    # def write(self, vals):
    #     result = super(LoginConfigSettings, self).write(vals)
    #     height=result.header_height_src+result.footer_height_src+result.body_login_height_src
    #     if height != 100:
    #         raise exceptions.ValidationError(_('The height value may not be incorrect'))
    #     return result


    _sql_constraints = [
        ('name_unique', 'unique(name)', _('The style name must be unique!')),
    ]