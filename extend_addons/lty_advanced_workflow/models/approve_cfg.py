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
        ], string='start status', required=False, default='draft')
    end_status =fields.Selection([
            ('draft', 'draft'),
            ('commited', 'commited'),
            ('approved', 'approved')
        ], string='end status', required=False, default='draft')
    company_id = fields.Many2one('res.company')
    status = fields.Selection([
            ('draft', 'draft'),
            ('commited', 'commited'),
            ('approved', 'approved')
        ], string='status', required=True, default='draft')
    line_ids = fields.One2many('lty.advanced.workflow.cfg.line','cfg_id', copy=True) 
    
    def do_confirm(self):    
        self.write({'status': 'commited'})
    def do_approve(self):    
        self.write({'status': 'approved'})    
    def do_cancel(self):    
        self.write({'status': 'draft'})        
    
    
class lty_advanced_workflow_cfg_line(models.Model):
    _name = 'lty.advanced.workflow.cfg.line'
    _order = 'squence'

    squence = fields.Integer(default=10)
    name = fields.Char(required=True)
    conditions = fields.Char(default='[()]', help='domain conditions')  
    approve_type =  fields.Selection([
            ('singel', 'singel'),
            ('mutil', 'mutil')
        ], string='Type', required=True, default='singel')
    approve_posts = fields.Many2many('employees.post', 'lty_wkf_cfg_line_post', 'post_id', 'approve_posts', 'Approve Post', help="")
    approve_post = fields.Many2one('employees.post','Approve Post', help="")
    approved_nubmber = fields.Char(default='1',readonly='1')
    farther_node = fields.Many2one('lty.advanced.workflow.cfg.line')
    next_node = fields.Many2one('lty.advanced.workflow.cfg.line')
    node_type = fields.Selection([
            ('start', 'start'),
            ('process', 'process'),
            ('stop', 'stop')
        ], string='Node Type', required=True, default='process')
    note = fields.Char()
    status = fields.Selection([
            ('open', 'open'),
            ('close', 'close')
        ], string='status', required=True, default='open')
    cfg_id = fields.Many2one('lty.advanced.workflow.cfg')    



    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100