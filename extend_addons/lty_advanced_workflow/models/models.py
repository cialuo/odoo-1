    # -*- coding: utf-8 -*-

from odoo import models, fields, api

class lty_advanced_workflow_cfg(models.Model):
    _name = 'lty.advanced.workflow.cfg'

    name = fields.Char()
    code = fields.Char()
    note = fields.Char()
    model = fields.Many2one('ir.model')
    start_status = fields.Char()
    end_status = fields.Char()
    company_id = fields.Many2one('res.company')
    status = fields.Char()    
    
class lty_advanced_workflow_cfg_line(models.Model):
    _name = 'lty.advanced.workflow.cfg.line'

    squence = fields.Integer()
    name = fields.Char()
    conditions = fields.Text()
    approve_type = fields.Char()
    approve_posts = fields.Char()
    approved_nubmber = fields.Char()
    next_node = fields.Char()
    node_type = fields.Char()
    note = fields.Char()
    status = fields.Char()	



    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100