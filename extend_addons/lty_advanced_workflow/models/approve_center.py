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
    commit_date = fields.Date()
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



    @api.multi
    def _active_wkf_node(self):
        #todo compute active status
        for user in self:
            user.active = True    
    @api.multi
    def do_approve(self):
        val_dict = {
            'name': '1234',
            'center_id': self.id,
            'user_id':self.env.user.id,
            'status':'approve',
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
                'status':'approve',
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
    
    
        