    # -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


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
    line_ids = fields.One2many('lty.advanced.workflow.cfg.line','cfg_id', copy=True, ondelete='cascade') 
    
    def do_confirm(self):    
        self.write({'status': 'commited'})
    def do_approve(self):
        for line in self.line_ids :
            try:
                self.env[line.cfg_id.model.model].search(eval(line.conditions),limit=1)
            except Exception,e:
                raise UserError((line.conditions+u'domain表达式错误!'))
                    
        self.write({'status': 'approved'})    
    def do_cancel(self):    
        self.write({'status': 'draft'})        
    
    
class lty_advanced_workflow_cfg_line(models.Model):
    _name = 'lty.advanced.workflow.cfg.line'
    _order = 'squence'

    squence = fields.Integer(default=10)
    name = fields.Char(required=True)
    conditions = fields.Char(required=True, help='domain conditions')  
    approve_type =  fields.Selection([
            ('singel', 'singel'),
            ('mutil', 'mutil')
        ], string='Type', required=True, default='singel')
    approve_posts = fields.Many2many('employees.post', 'lty_wkf_cfg_line_post', 'post_id', 'approve_posts', 'Approve Post', help="")
    approve_post = fields.Many2one('employees.post','Approve Post', help="")
    approved_nubmber = fields.Char(default='1',readonly='1')
    farther_node = fields.Many2one('lty.advanced.workflow.cfg.line', domain="[('cfg_id','=',cfg_id)]")
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
    cfg_id = fields.Many2one('lty.advanced.workflow.cfg',ondelete='cascade')    

    @api.onchange('conditions')
    def onchange_conditions(self):
        if self.cfg_id.model.model :
            if self.conditions  :
                try:
                    self.env[self.cfg_id.model.model].search(eval(self.conditions),limit=1)
                except Exception,e:
                    self.conditions = '' 
                    raise UserError((u'domain表达式错误！'+e.message))
                    return  {'warning': (e.message)}          
            
        #=======================================================================
        # if not self.product_id or self.product_qty < 0.0:
        #     self.product_qty = 0.0
        # if self.product_qty < self._origin.product_qty:
        #     return {'warning': _("By changing this quantity here, you accept the "
        #                          "new quantity as complete: Odoo will not "
        #                          "automatically generate a back order.")}
        #=======================================================================
    
    
    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100