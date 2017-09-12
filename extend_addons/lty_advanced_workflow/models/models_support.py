    # -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @api.multi
    def _adv_wkf_id_get(self):
        link_obj = self.env['lty.advanced.workflow.cfg']
        #return [(r.object, r.name) for r in link_obj.search([])]    
        return 1
    #adv_wkf_id = fields.Many2one('lty.advanced.workflow.cfg', default=_adv_wkf_id_get )
    adv_wkf_status = fields.Char()
    
    @api.model
    @api.multi
    def create(self, vals):
        productid = super(ProductTemplate, self).create(vals)
        obj_id = self.env['ir.model'].search([('model', 'ilike', self._name)], limit=1).id
        cfg_id =  self.env['lty.advanced.workflow.cfg'].search([('model', '=',obj_id)], limit=1).id
        for cfg_line in self.env['lty.advanced.workflow.cfg'].browse(cfg_id).line_ids :
            # print cfg_line
            val_dict = {
                'name': self.env['lty.advanced.workflow.cfg'].browse(cfg_id).code + '-' + productid.name + '-'+ str(cfg_line.squence),  
                'description':self.env['lty.advanced.workflow.cfg'].browse(cfg_id).name,                  
                'object_id': self._name + ',' +str(productid.id), 
                'approve_node':cfg_line.name,  
                'status':'commited',  
                'cfg_line_id':cfg_line.id,
                #'approve_posts': [(6,0,cfg_line.approve_posts.ids)],
                'approve_post': cfg_line.approve_post.id,
                'start_user': self.env.user.id,
            }
            self.env['lty.approve.center'].sudo().create(val_dict)
        return productid
    
    @api.multi
    def write(self, vals):
        approve_nodes = self.env['lty.approve.center'].search([('object_id', '=',self._name+','+str(self.id))])
        for node in approve_nodes :
            if node.approved is False  and node.active_node is True :
                raise UserError(('Approving is not done. '))   
        productid = super(ProductTemplate, self).write(vals)
    
        return productid
    
class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    total_qty = fields.Integer(compute='_compute_picking_total_qty',store=True)
    
    
    
    @api.one
    @api.depends('move_lines')
    def _compute_picking_total_qty(self):
        total_qty = 0
        for move_line in self.move_lines:
            total_qty = total_qty + move_line.price_unit*move_line.product_uom_qty
        
        self.total_qty = total_qty
    
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
        productid = super(stock_picking, self).create(vals)
        obj_id = self.env['ir.model'].search([('model', 'ilike', self._name)], limit=1).id
        cfg_id =  self.env['lty.advanced.workflow.cfg'].search([('model', '=',obj_id)], limit=1).id
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
            }
            self.env['lty.approve.center'].sudo().create(val_dict)
        return productid
    
    @api.multi
    def write(self, vals):
        approve_nodes = self.env['lty.approve.center'].search([('object_id', '=',self._name+','+str(self.id))])
        for node in approve_nodes :
            if node.approved is False  and node.active_node is True :
                raise UserError(('Approving is not done. '))   
        productid = super(stock_picking, self).write(vals)
    
        return productid
    
class purchase_order(models.Model):
    _inherit = 'purchase.order'
    
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
        productid = super(purchase_order, self).create(vals)
        obj_id = self.env['ir.model'].search([('model', 'ilike', self._name)], limit=1).id
        cfg_id =  self.env['lty.advanced.workflow.cfg'].search([('model', '=',obj_id)], limit=1).id
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
                
            }
            self.env['lty.approve.center'].sudo().create(val_dict)
            
        return productid
    
    @api.multi
    def write(self, vals):
        approve_nodes = self.env['lty.approve.center'].search([('object_id', '=',self._name+','+str(self.id))])
        for node in approve_nodes :
            if node.approved is False  and node.active_node is True :
                raise UserError(('Approving is not done. '))   
        productid = super(purchase_order, self).write(vals)
    
        return productid    
    
class PuchasePlan(models.Model):
    _inherit = 'purchase.plan'
    
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
        productid = super(PuchasePlan, self).create(vals)
        obj_id = self.env['ir.model'].search([('model', 'ilike', self._name)], limit=1).id
        cfg_id =  self.env['lty.advanced.workflow.cfg'].search([('model', '=',obj_id)], limit=1).id
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
                
            }
            self.env['lty.approve.center'].sudo().create(val_dict)
            
        return productid
    
    @api.multi
    def write(self, vals):
        approve_nodes = self.env['lty.approve.center'].search([('object_id', '=',self._name+','+str(self.id))])
        for node in approve_nodes :
            if node.approved is False  and node.active_node is True :
                raise UserError(('Approving is not done. '))   
        productid = super(PuchasePlan, self).write(vals)
    
        return productid 
    
    
       

class StockMove(models.Model):
    _inherit = 'stock.move'
    
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
        productid = super(StockMove, self).create(vals)
        obj_id = self.env['ir.model'].search([('model', 'ilike', self._name)], limit=1).id
        cfg_id =  self.env['lty.advanced.workflow.cfg'].search([('model', '=',obj_id)], limit=1).id
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
                
            }
            self.env['lty.approve.center'].sudo().create(val_dict)
            
        return productid
    
    @api.multi
    def write(self, vals):
        for stock_move in self :
            seconds = datetime.datetime.utcnow() - datetime.datetime.strptime(stock_move.create_date, "%Y-%m-%d %H:%M:%S")
            if seconds.seconds >5 :
                approve_nodes = stock_move.env['lty.approve.center'].search([('object_id', '=',stock_move._name+','+str(stock_move.id))])
                for node in approve_nodes :
                    if node.approved is False  and node.active_node is True :
                        raise UserError(('Approving is not done. '))   
        productid = super(StockMove, self).write(vals)
    
        return productid           
        
    
 
    