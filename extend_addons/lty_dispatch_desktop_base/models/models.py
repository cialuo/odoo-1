# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dispatch_control_desktop(models.Model):
    _name = 'dispatch.control.desktop'

    name = fields.Char()
    value = fields.Integer()
    description = fields.Text()
    user = fields.Many2one('res.users', default=lambda self: self.env.user.id, readonly='1')
    is_default = fields.Boolean(default=False)
    component_ids = fields.One2many('dispatch.control.desktop.component', 'desktop_id',  string="Desktop's components")
    
    def open_dispatch_desktop(self):
        return {
            'name': 'Desktop',
            'target': 'fullscreen',
            'tag' : 'dispatch_desktop.page',
            'type': 'ir.actions.client',
        }
           
class dispatch_control_desktop_component(models.Model):
    _name = 'dispatch.control.desktop.component'

    name = fields.Char()
    position_z_index = fields.Char()
    position_top = fields.Char()
    model_type = fields.Char()
    tem_display = fields.Char()
    position_left = fields.Char()
    line_id = fields.Many2one('route_manage.route_manage')
    desktop_id = fields.Many2one('dispatch.control.desktop', ondelete='restrict', string='Control Desktop')
	#备注
    remark = fields.Char()
	#显示顺序
    show_order = fields.Integer()
	#设备号
    on_bord_id = fields.Integer()
