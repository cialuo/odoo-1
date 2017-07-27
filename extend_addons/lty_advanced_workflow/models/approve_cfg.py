    # -*- coding: utf-8 -*-

from odoo import models, fields, api

class lty_advanced_workflow_cfg(models.Model):
    _name = 'lty.advanced.workflow.cfg'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    note = fields.Char()
    model = fields.Many2one('ir.model')
    start_status = fields.Selection([
            ('draft', 'draft'),
            ('commited', 'commited'),
            ('approved', 'approved')
        ], string='start status', required=True, default='draft')
    end_status =fields.Selection([
            ('draft', 'draft'),
            ('commited', 'commited'),
            ('approved', 'approved')
        ], string='end status', required=True, default='draft')
    company_id = fields.Many2one('res.company')
    status = fields.Selection([
            ('draft', 'draft'),
            ('commited', 'commited'),
            ('approved', 'approved')
        ], string='status', required=True, default='draft')
    line_ids = fields.One2many('lty.advanced.workflow.cfg.line','cfg_id') 
    
    def do_confirm(self):    
        self.write({'status': 'commited'})
    def do_approve(self):    
        self.write({'status': 'approved'})    
    
    
    
class lty_advanced_workflow_cfg_line(models.Model):
    _name = 'lty.advanced.workflow.cfg.line'

    squence = fields.Integer()
    name = fields.Char(required=True)
    conditions = fields.Char()
    approve_type =  fields.Selection([
            ('singel', 'singel'),
            ('mutil', 'mutil')
        ], string='Type', required=True, default='singel')
    approve_posts = fields.Char()
    approved_nubmber = fields.Char()
    next_node = fields.Many2one('lty.advanced.workflow.cfg.line')
    node_type = fields.Char()
    note = fields.Char()
    status = fields.Char()
    cfg_id = fields.Many2one('lty.advanced.workflow.cfg')



    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100