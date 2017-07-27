    # -*- coding: utf-8 -*-

from odoo import models, fields, api 
from odoo.exceptions import UserError



class lty_approve_center(models.Model):
    _name = 'lty.approve.center'
    _inherit = ['mail.thread']

    @api.multi
    def _links_get(self):
        link_obj = self.env['res.request.link']
        return [(r.object, r.name) for r in link_obj.search([])]

    name = fields.Char()
    commit_date = fields.Date(default=fields.Datetime.now)
    description = fields.Char()
    object_id = fields.Reference(
        string='Reference', selection=_links_get, 
        status={'commited': [('readonly', False)]}, ondelete="set null")
    source = fields.Char()
    approve_node = fields.Char()
    approve_opinions = fields.Char()
    status = fields.Selection([
            ('commited', 'commited'),
            ('approved', 'approved'),
            ('rejected', 'rejected')
        ], string='status', required=True, track_visibility='always', default='commited')
    line_ids = fields.One2many('lty.approve.logs','center_id') 
    cfg_line_id = fields.Many2one('lty.advanced.workflow.cfg.line')     
    active = fields.Boolean(compute='_active_wkf_node')
    approved = fields.Boolean(compute='_compute_approve_state') 



    @api.multi
    def _active_wkf_node(self):
        #todo compute active status
        farther_node_state = False
        if self.cfg_line_id.farther_node :
            object2 = self.object_id._name+','+str(self.object_id.id)
            farther_node_state = self.search([('object_id', '=',object2)], limit=1).approved                    
        domain = self.cfg_line_id.conditions.encode('gbk')                
        #self.env[self.object_id._name].search(domain, limit=1)
        
        if farther_node_state or not self.cfg_line_id.farther_node :
            for user in self:
                user.active = True   
            
    @api.multi
    def _compute_approve_state(self):
        #todo compute active status
        pp = 0
        for line in self.line_ids :
            if line.approve_status == 'approved':
                pp=pp+1
        if pp >= len(self.cfg_line_id.approved_nubmber) :
            for user in self:
                user.approved = True              
            
             
    @api.multi
    def do_approve(self):
        val_dict = {
            'name': '1234',
            'center_id': self.id,
            'user_id':self.env.user.id,
            'approve_status':'approved',
            'approve_opinions':self.approve_opinions,
        }
        self.env['lty.approve.logs'].create(val_dict)
        self.write({'status': 'approved','approve_opinions': ''})
    def do_reject(self):
        if not self.approve_opinions  :
            raise UserError(('Please input approve opinions. '))
        else:
            val_dict = {
                'name': '1234',
                'center_id': self.id,
                'user_id':self.env.user.id,
                'approve_status':'rejected',
                'approve_opinions':self.approve_opinions,
            }
            self.env['lty.approve.logs'].create(val_dict)            
            self.write({'status': 'rejected','approve_opinions': ''})
    
class lty_approve_logs(models.Model):
    _name = 'lty.approve.logs'

    name = fields.Char()     
    user_id = fields.Many2one('res.users')    
    approve_date = fields.Datetime(default=fields.Datetime.now)     
    approve_status = fields.Selection([
            ('approved', 'approved'),
            ('rejected', 'rejected')
        ], string='status')
    approve_opinions = fields.Char()
    center_id = fields.Many2one('lty.approve.center')       
    
    _sql_constraints = [
        ('user_uniq', 'unique (user_id,center_id)', 'You have approve or reject !'),
    ]    
    
    
        