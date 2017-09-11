    # -*- coding: utf-8 -*-

from odoo import models, fields, api 
from odoo.exceptions import UserError



class lty_approve_center(models.Model):
    _name = 'lty.approve.center'
    _inherit = ['mail.thread','ir.needaction_mixin']
    _order = 'status desc'

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
    active_node = fields.Boolean(compute='_active_wkf_node')
    approved = fields.Boolean(compute='_compute_approve_state')

    approve_posts = fields.Many2many('employees.post', 'lty_wkf_center_line_post', 'post_id', 'approve_posts', 'Approve Post', help="")
    approve_post = fields.Many2one('employees.post','Approve Post', help="")
    start_user = fields.Many2one('res.users')

    @api.model
    def _needaction_domain_get(self):
        return [('status', '=', 'commited'),('active_node', '=', True)]
    @api.multi
    def _active_wkf_node(self):
        #todo compute active status
        for user in self :
            farther_node_state = False
            condiction_state = False
            
            if user.cfg_line_id.farther_node :
                object2 = user.object_id._name+','+str(user.object_id.id)
                farther_node_state = self.search([('cfg_line_id', '=',user.cfg_line_id.farther_node.id),('object_id', '=',object2)]).approved
            else:
                farther_node_state = True
            
            domain = eval( user.cfg_line_id.conditions)
            domain.append(('id', '=', user.object_id.id))                    
            if len(self.env[user.object_id._name].search(domain))>0 :
                condiction_state = True
            
            if condiction_state and farther_node_state :
                user.active_node = True
            
    @api.multi
    def _compute_approve_state(self):
        #todo compute active status
        for user in self:
            pp = len(self.env['lty.approve.logs'].search([('center_id', '=',user.id),('approve_status', '=','approved')]))
            if pp >= int(user.cfg_line_id.approved_nubmber) :
                user.approved = True
           
    @api.multi
    def do_approve(self):
        if not self.active_node  :
            raise UserError(('This node is not start!. '))         
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
        if not self.active_node  :
            raise UserError(('This node is not start!. '))        
        if not self.approve_opinions  :
            raise UserError(('Please input approve opinions. '))
        else:
            val_dict = {
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
    
    
        