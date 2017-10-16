    # -*- coding: utf-8 -*-

from odoo import models, fields, api 
from odoo.exceptions import UserError

class lty_approve_center_group(models.Model):
    _name = 'lty.approve.center.group'

    @api.multi
    def _links_get(self):
        link_obj = self.env['res.request.link']
        return [(r.object, r.name) for r in link_obj.search([])]

    name = fields.Char()     
    center_id = fields.One2many('lty.approve.center','center_id','center_id',domain=['|',('active', '=', False),('active', '=', True)]) 
    start_user = fields.Many2one('res.users')
    object_id = fields.Reference(
        string='Reference', selection=_links_get, 
        status={'commited': [('readonly', False)]}, ondelete="set null")
    cfg_id = fields.Many2one('lty.advanced.workflow.cfg')
    status = fields.Selection([
            ('approving', u'审批中'),
            ('rejected', u'拒绝'),
            ('cancel', u'取消'),
            ('done', u'完成')
        ], string=u'状态', required=True, track_visibility='always', default='approving')
    
    @api.multi
    def do_reset(self):
        if  self.status != 'done' :
            self.env['lty.approve.center'].search([('center_id','=',self.id)])
            for node in self.center_id :
                #node.unlink()
                node.sudo().write({'status': 'cancel','cfg_line_id': '', 'cfg_father_line_id': ''})  
            for node_false in self.sudo().env['lty.approve.center'].search([('center_id','=',self.id),('active','=',False)]) :
                #node_false.unlink()
                node_false.sudo().write({'status': 'cancel','cfg_line_id': '', 'cfg_father_line_id': ''})  
        else:
            raise UserError((u'该流程已审批完成，禁止取消!. '))

        self.sudo().object_id.write({'approve_state': u'审批被取消'})
        self.sudo().write({'status': 'cancel'})  
        #self.write({'status': 'approved','approve_opinions': ''})    

    @api.multi
    def do_reopen(self):
        self.do_reset()
        productid = self.object_id
        cfg_id =  self.cfg_id.id
        for cfg_line in self.env['lty.advanced.workflow.cfg'].browse(cfg_id).line_ids :
            # print cfg_line
            val_dict = {
                'name': self.env['lty.advanced.workflow.cfg'].browse(cfg_id).code + '-' + productid.name + '-'+ str(cfg_line.squence),  
                'description':self.env['lty.advanced.workflow.cfg'].browse(cfg_id).name,                  
                'object_id': productid._name + ',' +str(productid.id), 
                'approve_node':cfg_line.name,  
                'status':'commited',  
                'cfg_line_id':cfg_line.id,
                'cfg_father_line_id':cfg_line.farther_node.id,
                #'approve_posts': [(6,0,cfg_line.approve_posts.ids)],
                'approve_post': cfg_line.approve_post.id,
                'start_user': self.env.user.id,
                'center_id': self.id,
                
            }
            self.env['lty.approve.center'].sudo().create(val_dict)

        self.sudo().write({'status': 'approving'})  
    
    
class lty_approve_center(models.Model):
    _name = 'lty.approve.center'
    _inherit = ['mail.thread','ir.needaction_mixin']
    _order = 'name desc'

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
            ('rejected', 'rejected'),
            ('cancel', u'取消')
        ], string='status', required=True, track_visibility='always', default='commited')
    line_ids = fields.One2many('lty.approve.logs','center_id') 
    cfg_line_id = fields.Many2one('lty.advanced.workflow.cfg.line')
    # 上级工作流节点
    cfg_father_line_id = fields.Many2one('lty.advanced.workflow.cfg.line')
    #上级节点状态
    father_node_state = fields.Boolean()
    #节点激活状态
    active_node = fields.Boolean(compute='_active_wkf_node')
    #是否显示
    active = fields.Boolean(compute='_compute_node_active', store = True)
    #是否通过
    approved = fields.Boolean(compute='_compute_approve_state')
    #审批岗位
    approve_posts = fields.Many2many('employees.post', 'lty_wkf_center_line_post', 'post_id', 'approve_posts', 'Approve Post', help="")
    #审批岗位
    approve_post = fields.Many2one('employees.post','Approve Post', help="")
    #发起人
    start_user = fields.Many2one('res.users')
    center_id = fields.Many2one('lty.approve.center.group')
    
    
    @api.one
    @api.depends('active_node')
    def _compute_node_active(self):
        for user in self :
            user.active = user.active_node        
        
        #total_qty = 0
        #for move_line in self.move_lines:
        #    total_qty = total_qty + move_line.product_uom_qty
        
        #self.total_qty = total_qty
            
        
    @api.model
    def _needaction_domain_get(self):
        return [('status', '=', 'commited'),('active_node', '=', True),('approved', '=', False)]
    @api.multi
    def _active_wkf_node(self):
        #todo compute active status
        for user in self :
            farther_node_state = False
            condiction_state = False
            
            if user.cfg_line_id.farther_node :
                object2 = user.object_id._name+','+str(user.object_id.id)
                farther_node_state = self.sudo().search([('cfg_line_id', '=',user.cfg_line_id.farther_node.id),('object_id', '=',object2)],limit = 1).approved
            else:
                farther_node_state = True
            if user.cfg_line_id:                           
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
            raise UserError((u'审批节点未被激活!. '))
        if self.env.user.employee_post.id != self.approve_post.id :
            raise UserError((u'您 没有权限进行审批!. '))        
        #更新下级流程节点状态
        next_nodes = self.sudo().search([('active', '=',False),('status', '<>','cancel'),('cfg_father_line_id', '=',self.cfg_line_id.id),('object_id', '=',self.object_id._name+','+str(self.object_id.id))])
        next_nodes.active_node
        if  next_nodes :       
            for next_node in next_nodes:
                #todo 这里需要判断下节点人数
                domain = eval( next_nodes.cfg_line_id.conditions)
                domain.append(('id', '=', next_nodes.object_id.id))
                if self.sudo().env[next_nodes.object_id._name].search(domain):
                    next_node.sudo().write({'active': True})
                else:
                    self.sudo().center_id.write({'status': 'done'})
        else :
            self.sudo().center_id.write({'status': 'done'})
        self.sudo().object_id.write({'approve_state': u'审批节点'+':'+self.approve_node + u'通过'}) 
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
        if self.env.user.employee_post.id != self.approve_post.id :
            raise UserError((u'您 没有权限进行审批!. '))            
        if not self.approve_opinions  :
            raise UserError((u'拒审必须输入原因. '))         
        if not self.active_node  :
            raise UserError((u'审批节点未被活活!. '))             
        else:
            for next_node in self.search([('active', '=',False),('cfg_father_line_id', '=',self.cfg_line_id.id),('object_id', '=',self.object_id._name+','+str(self.object_id.id))]):
                #todo 这里需要判断下节点人数
                next_node.write({'active': False})
                #next_node.sudo().center_id.write({'status': 'rejected'})                                
            val_dict = {
                'center_id': self.id,
                'user_id':self.env.user.id,
                'approve_status':'rejected',
                'approve_opinions':self.approve_opinions,
            }
            self.sudo().env['lty.approve.logs'].create(val_dict)            
            self.sudo().write({'status': 'rejected','approve_opinions': ''})
            #更新当前节点对应的组状态为拒绝
            self.sudo().center_id.write({'status': 'rejected'})                                
        self.sudo().object_id.write({'approve_state': u'审批节点'+':'+self.approve_node + u'拒绝'})  
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
    
    
        