# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FaultCategory(models.Model):
    """
    故障分类
    """
    _name = 'fleet_manage_fault.fault_category'
    
    fault_category_code = fields.Char("Fault Category Code",help='Fault Category Code')
    name = fields.Char("Fault Category Name",help='Fault Category Name')
    user_id = fields.Many2one('res.users',string="Create Name")
    create_date = fields.Date("Create Date",help='Create Date')
    state = fields.Selection([
       ('draft', "Draft"),
       ('use', "Use"),
       ('done', "Done"),],default='use')
    
    active = fields.Boolean(default=True)
    appearance_ids = fields.One2many(
       'fleet_manage_fault.fault_appearance', 'category_id', string="appearances")
    
    reason_ids = fields.One2many(
       'fleet_manage_fault.fault_reason', 'category_id', string="reasons",domain=[('appearance_id','=',None)])
    
    @api.multi
    def action_draft(self):
        self.state = 'draft'
        
    @api.multi
    def action_use(self):
        self.state = 'use'
        self.active = True
        
    @api.multi
    def action_done(self):
        self.state = 'done'
        self.active = False


class FaultAppearance(models.Model):
    """
    故障现象
    """
    _name = 'fleet_manage_fault.fault_appearance'
    
    fault_appearance_code = fields.Char("Fault appearance Code",help='Fault appearance Code')
    name = fields.Char("Fault appearance Name", help='Fault appearance Name')   
    user_id = fields.Many2one('res.users',string="Create Name")
    create_date = fields.Date("Create Date",help='Create Date')
    state = fields.Selection([
       ('draft', "Draft"),
       ('use', "Use"),
       ('done', "Done"),],default='use')
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('fleet_manage_fault.fault_category',
        ondelete='cascade', string="Fault Category Name")
    
    reason_ids = fields.One2many(
       'fleet_manage_fault.fault_reason', 'appearance_id', string="Reasons")
    sequence = fields.Integer("Sequence", help="Sequence")

    reason_ct = fields.Integer(string="Fault Reason Count", compute='_get_reason_count')

    @api.depends("reason_ids")
    def _get_reason_count(self):
        if self.reason_ids:
            self.reason_ct = len(self.reason_ids)
        else:
            self.reason_ct = 0


class FaultReason(models.Model):
    """
    故障原因
    """
    _name = 'fleet_manage_fault.fault_reason'
    
    fault_reason_code = fields.Char("Fault Reason Code",help='Fault Reason Code')
    name = fields.Char("Fault Reason Name", help='Fault Reason Name') 
    user_id = fields.Many2one('res.users',string="Create Name")
    create_date = fields.Date("Create Date",help='Create Date')
    state = fields.Selection([
       ('draft', "Draft"),
       ('use', "Use"),
       ('done', "Done"),],default='use')    
    active = fields.Boolean(default=True)
    appearance_id = fields.Many2one('fleet_manage_fault.fault_appearance',
        ondelete='cascade', string="Fault appearance Name")
    
    category_id = fields.Many2one('fleet_manage_fault.fault_category',
        ondelete='cascade', string="Fault Category Name")
    
    method_ids = fields.One2many(
       'fleet_manage_fault.fault_method', 'reason_id', string="methods")
    sequence = fields.Integer("Sequence", help="Sequence")
    method_ct = fields.Integer(string="Fault Method Count", compute='_get_method_count')

    @api.depends("method_ids")
    def _get_method_count(self):
        if self.method_ids:
            self.method_ct = len(self.method_ids)
        else:
            self.method_ct = 0
    
    @api.onchange('appearance_id')
    def onchange_appearance_id(self):
        if self.appearance_id and not self.category_id:
            self.category_id = self.appearance_id.category_id


class FaultMethod(models.Model):
    """
    维修办法
    """
    _name = 'fleet_manage_fault.fault_method'
    
    fault_method_code = fields.Char("Fault Method Code",help='Fault Method Code')
    name = fields.Char("Fault Method Name", help='Fault Method Name')
    user_id = fields.Many2one('res.users',string="Create Name")
    create_date = fields.Date("Create Date",help='Create Date')
    state = fields.Selection([
       ('draft', "Draft"),
       ('use', "Use"),
       ('done', "Done"),], default='use')
    active = fields.Boolean(default=True)
    remark = fields.Text("Remark", help='Remark')
    work_time = fields.Integer(string="Work Time(Minutes)")
    warranty_deadline = fields.Integer(string="Warranty Deadline(Days)")
    complex_level = fields.Selection([
       ('1 work', "One work"),
       ('2 works', "Two works"),
       ('group works', "Group Works"),],default='1 work')  
    materials_control = fields.Boolean("Materials Control")
    state = fields.Selection([
       ('draft', "Draft"),
       ('use', "Use"),
       ('done', "Done"),], default='use')
    
    reason_id = fields.Many2one('fleet_manage_fault.fault_reason',
        ondelete='cascade', string="Fault reason Name",required=True)
    appearance_id = fields.Many2one('fleet_manage_fault.fault_appearance',
        ondelete='cascade', string="Fault appearance Name")
    category_id = fields.Many2one('fleet_manage_fault.fault_category',
        ondelete='cascade', string="Fault Category Name")
    avail_ids = fields.One2many(
       'fleet_manage_fault.available_product', 'reason_id', string="Products")
    
    @api.onchange('reason_id')
    def onchange_reason_id(self):
        if self.reason_id and not self.category_id:
            self.category_id = self.reason_id.category_id
            self.appearance_id = self.reason_id.appearance_id


class AvailableProduct(models.Model):
    _name = 'fleet_manage_fault.available_product'

    product_id = fields.Many2one('product.product',string="Product")

    name = fields.Char(required=True)    
    reason_id = fields.Many2one('fleet_manage_fault.fault_method',
        ondelete='cascade', string="Fault Reason Name")
    default_dosage = fields.Integer("Default Dosage")
    max_dosage = fields.Integer("Default Dosage")
    remark = fields.Text("Remark", help="Remark")

    product_code = fields.Text("Product Code", help="Product Code")
    product_name = fields.Text("Product Name", help="Product Name")
    product_type = fields.Text("Product Type", help="Product Type")
    product_size = fields.Text("Product Size", help="Product Size")
    product_unit = fields.Text("Product Unit", help="Product Unit")


    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_code = self.product_id.code
            self.product_name = self.product_id.name
        else:
            self.product_code = ''
            self.product_name = ''
