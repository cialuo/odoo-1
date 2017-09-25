# -*- coding: utf-8 -*-

from odoo import models, fields, api

class cheshi_odoo(models.Model):
#     _name = 'cheshi_odoo.cheshi_odoo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
      WORKFLOW_STATE_SELECTION = [
        ('draft', '草稿'),
        ('confirm', '确认'),
        ('complete', '完成')
    ]

      _name = "ceshi.ceshi"
      name  = fields.Char(string="申请人")
      days  = fields.Integer(string="天数")
      startdate = fields.Date(string="开始日期")
      reason = fields.Text(string="请假事由")
      state = fields.Selection(WORKFLOW_STATE_SELECTION, default = "draft",string = "状态",readonly = True)

      # state = fields.Selection(WORKFLOW_STATE_SELECTION)

      @api.multi
      def do_draft(self):
            self.state = "draft"
      
      @api.multi
      def do_confirm(self):
            self.state = "confirm"

      @api.multi
      def do_complete(self):
            self.state = "complete"
# 二级菜单定义对象+属性
# 三级菜单