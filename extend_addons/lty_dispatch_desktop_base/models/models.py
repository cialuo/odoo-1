# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dispatch_control_desktop(models.Model):
    _name = 'dispatch.control.desktop'

    name = fields.Char()
    value = fields.Integer()
    color = fields.Integer()
    description = fields.Text()
    user = fields.Many2one('res.users', default=lambda self: self.env.user.id, readonly='1')
    is_default = fields.Boolean(default=False)
    component_ids = fields.One2many('dispatch.control.desktop.component', 'desktop_id',  string="Desktop's components")
    #资源字体颜色
    src_font_conf =  fields.Char(default='#a3a6ad')
    #配车数量
    applycar_num = fields.Boolean(default=True)
    #机动车辆
    active_car= fields.Boolean(default=True)
    #维保停运
    main_outage = fields.Boolean(default=True)
    #共享机动
    share_active_car = fields.Boolean(default=True)
    #信号在线
    signal_online = fields.Boolean(default=True)
    #信号掉线
    signal_outline = fields.Boolean(default=True)
    #司机
    car_driver = fields.Boolean(default=True)
    #乘务员
    car_attendant = fields.Boolean(default=True)
    # 挂车数量
    trailerNum = fields.Boolean(default=True)
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
    #线路ID
    line_id = fields.Many2one('route_manage.route_manage')
    #控制台ID
    desktop_id = fields.Many2one('dispatch.control.desktop',ondelete='cascade', string='Control Desktop')
    #备注
    remark = fields.Char()
    #显示顺序
    show_order = fields.Integer()
    #设备号
    on_bord_id = fields.Integer()
