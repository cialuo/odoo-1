# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dispatch_control_desktop(models.Model):
    _name = 'dispatch.control.desktop'

    name = fields.Char()
    value = fields.Integer()
    description = fields.Text()
    user = fields.Many2one('res.users', default=lambda self: self.env.user.id)
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
    position_left = fields.Char()
    desktop_id = fields.Many2one('dispatch.control.desktop', ondelete='restrict', string='Control Desktop')
