# -*- coding: utf-8 -*-

from odoo.addons.board.controllers.main import Board
from odoo.http import Controller, route, request
class MyBoard(Board):
    @route()
    def add_to_dashboard(self, action_id, context_to_save, domain, view_mode, name=''):

        """
            复写收藏的函数,把仪表盘数据存入库
        :param action_id:
        :param context_to_save:
        :param domain:
        :param view_mode:
        :param name:
        :return:
        """
        super(MyBoard,self).add_to_dashboard(action_id,context_to_save,domain,view_mode,name)
        action = request.env.ref('board.open_board_my_dash_action')

        if action and action['res_model'] == 'board.board' and action['views'][0][1] == 'form':
            view_id = action['views'][0][0]
            board = request.env['board.board'].fields_view_get(view_id, 'form')
            if board and 'arch' in board:
                request.env['dashboard.chart_views'].create({
                    'name': str(action_id),
                    'str': name,
                    'view_mode': view_mode,
                    'context': str(context_to_save),
                    'domain': str(domain)
                })

                return True
        return False