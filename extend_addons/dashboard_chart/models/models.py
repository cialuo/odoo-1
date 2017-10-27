# -*- coding: utf-8 -*-
from xml.etree import ElementTree
from odoo import models,api,fields,exceptions,_

class ChartViews(models.Model):

    _name = 'dashboard.chart_views'
    _description = 'Chart Views'
    _rec_name = 'str'

    """
        看板的视图集合,用于保存收藏的仪表盘
    """

    name = fields.Char()

    str = fields.Char()

    view_mode = fields.Char()

    context = fields.Char()

    domain = fields.Char()

    @api.multi
    def unlink(self):
        boards = self.env['dashboard.board_setting'].search([])
        # 重载删除方法
        for item in self:
                for board in boards:
                    if board.view_ids.filtered(lambda r:r.id == item.id):
                        raise exceptions.UserError(u'%s被引用,删除失败!' % (item.str))

        return super(ChartViews, self).unlink()




class Dashboard(models.Model):

    _name = 'dashboard.board_setting'
    _description = 'Dashboard Setting'
    _sql_constraints = [('menu_id_unique', 'unique (menu_id)', u'菜单已经存在看板!')]
    """
        看板数据:
            用于保存界面创建的看板数据
    """

    name = fields.Char(required=True)

    menu_id = fields.Many2one('ir.ui.menu',domain=['&',('sequence','=',-1),('name','ilike',u'看板')],required=True)

    view_ids = fields.Many2many('dashboard.chart_views')

    @api.multi
    def using_board(self):
        """

            应用看板模板

        :return:
        """
        for setting in self:
            action = setting.menu_id.action
            if action and action['res_model'] == 'board.board' and action['views'][0][1] == 'form':
                view_id = action['views'][0][0]
                board = self.env['board.board'].fields_view_get(view_id, 'form')
                if board and 'arch' in board:
                    xml = ElementTree.fromstring(board['arch'])
                    columns = xml.findall('./board/column')
                    if columns is not None :
                        #删除原本的值
                        views = self.remove_element(columns,setting)
                        #新增视图
                        for view in views:
                            new_action = ElementTree.Element('action', {
                                'name': view.name,
                                'string': view.str,
                                'view_mode': view.view_mode,
                                'context': view.context,
                                'domain': view.domain
                            })
                            columns[0].append(new_action)

                        self._arch_preprocessing(xml, view_id)

    def remove_element(self, columns, setting):
        """
            对比配置对象和列对象进行删除
        :param columns:
        :param setting:
        :return:
        """
        views = list()
        #看板配置：用于匹配
        ids = setting.view_ids.mapped('name')
        names = setting.view_ids.mapped('view_mode')
        #界面上的看板集合
        element_ids = list()
        element_names = list()
        for column in columns:
            #如果设置不存在就清除所有试图
            if len(ids) == 0:
                column.clear()

            # 删除在看板设置内不存在的节点
            for element in column._children:
                element_ids.append(element.get('name'))
                element_names.append(element.get('view_mode'))
                if ids.count(element.get('name')) == 0 or (ids.count(element.get('name')) > 0 and names.count(element.get('view_mode')) ==0):
                   column.remove(element)

        # 筛选出在节点内不存在的试图
        for view in setting.view_ids:
            if element_ids.count(str(view.name)) == 0 or (element_ids.count(str(view.name)) > 0 and element_names.count(str(view.view_mode)) == 0):
               views.append(view)

        return views

    def _arch_preprocessing(self,xml,view_id):
        """
            保存xml
        :return:
        """
        arch = ElementTree.tostring(xml, 'utf-8')
        self.env['ir.ui.view.custom'].create({
            'user_id': self.env.uid,
            'ref_id': view_id,
            'arch': arch
        })
