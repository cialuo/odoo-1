    # -*- coding: utf-8 -*-

from odoo import models, fields, api

class lty_advanced_workflow_approve_center(models.Model):
    _name = 'lty.advanced.workflow.approve.center'
    _inherit = ['mail.thread']

    @api.multi
    def _links_get(self):
        link_obj = self.env['res.request.link']
        return [(r.object, r.name) for r in link_obj.search([])]

    @api.one
    @api.depends('object_id')
    def _get_product(self):
        if self.object_id and self.object_id._name == 'product.product':
            self.product = self.object_id
        else:
            self.product = False

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
    @api.multi
    def do_approve(self):    
        self.write({'status': 'approved'})
    def do_reject(self):    
        self.write({'status': 'rejected'})
        
        
    
 
    