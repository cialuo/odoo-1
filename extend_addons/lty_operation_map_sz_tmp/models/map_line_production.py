# -*- coding: utf-8 -*-

from odoo import models, fields, api

class map_line_production_info(models.Model):
    _name = 'map.line.production.info'

    #配置名称
    name = fields.Char()
    #线路ID
    line_id = fields.Many2one('route_manage.route_manage')
    #线路方向
    direction = fields.Selection([('up', 'up'), ('down', 'down')])
    #地图数据
    map_data = fields.Text()
    #地图数据v2
    map_data_v2 = fields.Text()
    #线路线条颜色
    tools_line_color = fields.Char()
    #线路线条宽度
    tools_line_width = fields.Char()
    #线路是否显示
    tools_line_display = fields.Boolean()		
    #站台字体
    tools_station_font_family = fields.Char()
    #站台字体颜色
    tools_station_font_color = fields.Char()
    #站台字体样式
    tools_station_font_style= fields.Char()
    #站台字体样式颜色
    tools_station_font_style_color= fields.Char()	
    #站台是否显示
    tools_station_is_display= fields.Boolean()
    #站台名称是否显示
    tools_station_name_is_display= fields.Boolean()
    #轨迹导入颜色
    tools_import_trajectory_color= fields.Boolean()
    #轨迹导入宽度
    tools_import_trajectory_width= fields.Boolean()