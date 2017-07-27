    # -*- coding: utf-8 -*-

from odoo import models, fields, api

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
            print cfg_line
            val_dict = {
                'name': self.env['lty.advanced.workflow.cfg'].browse(cfg_id).code + '-' + productid.name + '-'+ str(cfg_line.squence),  
                'description':self.env['lty.advanced.workflow.cfg'].browse(cfg_id).name,                  
                'object_id': self._name + ',' +str(productid.id), 
                'approve_node':cfg_line.name,  
                'status':'commited',  
                'cfg_line_id':cfg_line.id,                               
            }
            self.env['lty.approve.center'].create(val_dict)
        return productid  



        
        
    
 
    