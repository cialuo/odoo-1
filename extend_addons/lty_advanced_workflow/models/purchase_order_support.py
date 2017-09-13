    # -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime
    
class purchase_order(models.Model):
    _inherit = 'purchase.order'
	
	
    approve_state = fields.Char(u'审批状态',track_visibility='always')
    
    @api.multi
    def _adv_wkf_id_get(self):
        link_obj = self.env['lty.advanced.workflow.cfg']
        #return [(r.object, r.name) for r in link_obj.search([])]    
        return 1
    #adv_wkf_id = fields.Many2one('lty.advanced.workflow.cfg', default=_adv_wkf_id_get )
    #adv_wkf_status = fields.Char()
    
    @api.model
    @api.multi
    def create(self, vals):
        if vals:
            vals.update({
                'approve_state': u'单据进入审批状态，此期间禁止任何修改',
            })        
        
        productid = super(purchase_order, self).create(vals)
        obj_id = self.env['ir.model'].search([('model', 'ilike', self._name)], limit=1).id
        cfg =  self.env['lty.advanced.workflow.cfg'].search([('model', '=',obj_id),('status','=','approved')], limit=1)
        cfg_id =  cfg.id
        group_val_dict = {
            'object_id': self._name + ',' +str(productid.id), 
            'start_user': self.env.user.id,
            'name': cfg.code+'-'+productid.name,
            'cfg_id': cfg_id,
        }
        #center_id = self.env['lty.approve.center.group'].sudo().create(group_val_dict) 
        center_id = self.env['lty.approve.center.group'].sudo().create(group_val_dict).id
        for cfg_line in self.env['lty.advanced.workflow.cfg'].browse(cfg_id).line_ids :
            # print cfg_line
            val_dict = {
                'name': self.env['lty.advanced.workflow.cfg'].browse(cfg_id).code + '-' + productid.name + '-'+ str(cfg_line.squence),  
                'description':self.env['lty.advanced.workflow.cfg'].browse(cfg_id).name,                  
                'object_id': self._name + ',' +str(productid.id), 
                'approve_node':cfg_line.name,  
                'status':'commited',  
                'cfg_line_id':cfg_line.id,
                'cfg_father_line_id':cfg_line.farther_node.id,
                #'approve_posts': [(6,0,cfg_line.approve_posts.ids)],
                'approve_post': cfg_line.approve_post.id,
                'start_user': self.env.user.id,
                'center_id': center_id,
            }
            self.env['lty.approve.center'].sudo().create(val_dict)
        return productid
    
    @api.multi
    def write(self, vals):
        approve_nodes = self.env['lty.approve.center'].search([('object_id', '=',self._name+','+str(self.id))])
        if not vals.get('approve_state'):
            for node in approve_nodes :
                if node.approved is False  and node.active_node is True :
                    raise UserError((u'审批未完成或被拒绝. '))   
        productid = super(purchase_order, self).write(vals)
    
        return productid   