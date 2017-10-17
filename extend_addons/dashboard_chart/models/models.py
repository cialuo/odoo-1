# -*- coding: utf-8 -*-

from odoo import models,api,fields

class ChartViews(models.Model):

    _name = 'dashboard.chart_views'
    _description = 'Chart Views'

    """
        看板的视图集合,用于保存收藏的仪表盘
    """

    name = fields.Char()

    str = fields.Char()

    view_mode = fields.Char()

    context = fields.Char()

    domain = fields.Char()


class Dashboard(models.Model):

    _name = 'dashboard.board_setting'
    _description = 'Dashboard Setting'

    """
        看板数据:
            用于保存界面创建的看板数据
    """

    name = fields.Char()

    menu_id = fields.Many2one('ir.ui.menu')

    view_id = fields.Many2many('dashboard.chart_views')

