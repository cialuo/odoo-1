    # -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @api.multi
    def _adv_wkf_id_get(self):
        link_obj = self.env['lty.advanced.workflow.cfg']
        #return [(r.object, r.name) for r in link_obj.search([])]    
        return 1
    adv_wkf_id = fields.Many2one('lty.advanced.workflow.cfg', default=_adv_wkf_id_get )
    adv_wkf_status = fields.Char()
    
    @api.model
    @api.multi
    def create(self, vals):
        productid = super(ProductTemplate, self).create(vals)
        productid.id
        self._name
        self._name
        cfg_obj = self.env['lty.advanced.workflow.cfg']
        cfg_obj.search([('model', 'ilike', '')], limit=1)
        
        
        
        return productid  



        
        
    
 
    