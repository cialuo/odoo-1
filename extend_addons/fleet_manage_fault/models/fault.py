# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FaultCategory(models.Model):
    """
    故障分类
    """
    _name = 'fleet_manage_fault.fault_category'
    _sql_constraints = [('code_uniq', 'unique (fault_category_code)', "Category code already exists !")]

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    fault_category_code = fields.Char("Fault Category Code", help='Fault Category Code',required=True)
    name = fields.Char("Fault Category Name", help='Fault Category Name',required=True)
    user_id = fields.Many2one('hr.employee', string="Create Name",default=_default_employee, required=True,readonly=True)
    create_date = fields.Date("Create Date",help='Create Date',default=fields.Date.context_today,readonly=True)
    state = fields.Selection([('use', "Use"), ('done', "Done")], default='use')
    
    active = fields.Boolean(default=True)
    appearance_ids = fields.One2many(
       'fleet_manage_fault.fault_appearance', 'category_id', string="appearances")
    
    reason_ids = fields.One2many(
       'fleet_manage_fault.fault_reason', 'category_id', string="reasons",domain=[('appearance_id','=',None)])

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
    _sql_constraints = [('code_uniq', 'unique (inner_code)', "Appearance code already exists !")]

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    inner_code = fields.Char("Inner Code", help='Inner Code', required=True)
    fault_appearance_code = fields.Char("Fault appearance Code",compute="_get_fault_code",
                                        help='Fault appearance Code',required=True)
    name = fields.Char("Fault appearance Name", help='Fault appearance Name',required=True)
    user_id = fields.Many2one('hr.employee', string="Create Name", default=_default_employee, required=True,
                              readonly=True)
    create_date = fields.Date("Create Date", help='Create Date', default=fields.Date.context_today, readonly=True)

    state = fields.Selection([('use', "Use"),('done', "Done")], default='use')
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('fleet_manage_fault.fault_category', ondelete='cascade',
                                  string="Fault Category Name", required=True)
    
    reason_ids = fields.One2many(
       'fleet_manage_fault.fault_reason', 'appearance_id', string="Reasons")
    sequence = fields.Integer("Sequence", default=1, help="Sequence", readonly=True)

    reason_ct = fields.Integer(string="Fault Reason Count", compute='_get_reason_count')

    @api.depends("inner_code")
    def _get_fault_code(self):
        for i in self:
            if i.category_id and i.inner_code:
                i.fault_appearance_code = i.category_id.fault_category_code+i.inner_code

    @api.multi
    def action_use(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.active = False

    @api.depends("reason_ids")
    def _get_reason_count(self):
        for i in self:
            if i.reason_ids:
                i.reason_ct = len(i.reason_ids)
            else:
                i.reason_ct = 0

    @api.model
    def create(self, vals):
        if vals.get('category_id'):
            category = self.env['fleet_manage_fault.fault_category'].browse(vals.get('category_id'))
            vals['sequence'] = len(category.appearance_ids)+1
        return super(FaultAppearance, self).create(vals)


class FaultReason(models.Model):
    """
    故障原因
    """
    _name = 'fleet_manage_fault.fault_reason'
    _sql_constraints = [('code_uniq', 'unique (inner_code)', "Reason code already exists !")]

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    inner_code = fields.Char("Inner Code", help='Inner Code', required=True)
    fault_reason_code = fields.Char("Fault Reason Code",help='Fault Reason Code',
                                    compute="_get_fault_code",required=True)
    name = fields.Char("Fault Reason Name", help='Fault Reason Name',required=True)
    user_id = fields.Many2one('hr.employee', string="Create Name", default=_default_employee, required=True,
                              readonly=True)
    create_date = fields.Date("Create Date", help='Create Date', default=fields.Date.context_today, readonly=True)
    state = fields.Selection([('use', "Use"),('done', "Done")], default='use')
    active = fields.Boolean(default=True)
    appearance_id = fields.Many2one('fleet_manage_fault.fault_appearance',
                                    ondelete='cascade', string="Fault appearance Name")
    category_id = fields.Many2one('fleet_manage_fault.fault_category',
                                    ondelete='cascade', string="Fault Category Name", required=True)
    
    method_ids = fields.One2many('fleet_manage_fault.fault_method', 'reason_id', string="methods")
    sequence = fields.Integer("Sequence", help="Sequence", readonly=True)
    method_ct = fields.Integer(string="Fault Method Count", compute='_get_method_count')

    @api.depends("inner_code",'appearance_id.fault_appearance_code','category_id.fault_category_code')
    def _get_fault_code(self):
        for i in self:
            if i.inner_code:
                if i.appearance_id:
                    i.fault_reason_code = i.appearance_id.fault_appearance_code+i.inner_code
                elif i.category_id:
                    i.fault_reason_code = i.category_id.fault_category_code+i.inner_code

    @api.multi
    def action_use(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.active = False

    @api.depends("method_ids")
    def _get_method_count(self):
        for i in self:
            if i.method_ids:
                i.method_ct = len(i.method_ids)
            else:
                i.method_ct = 0
    
    @api.onchange('appearance_id')
    def onchange_appearance_id(self):
        if self.appearance_id:
            self.category_id = self.appearance_id.category_id

    @api.model
    def create(self, vals):
        if vals.get("appearance_id",''):
            appearance = self.env['fleet_manage_fault.fault_appearance'].browse(vals.get('appearance_id'))
            vals['sequence'] = len(appearance.reason_ids) + 1
        elif vals.get('category_id',''):
            category = self.env['fleet_manage_fault.fault_category'].browse(vals.get('category_id'))
            vals['sequence'] = len(category.reason_ids) + 1

        return super(FaultReason, self).create(vals)


class FaultMethod(models.Model):
    """
    维修办法
    """
    _name = 'fleet_manage_fault.fault_method'
    _sql_constraints = [('code_uniq', 'unique (inner_code)', "Method code already exists !")]

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    inner_code = fields.Char("Inner Code", help='Inner Code', required=True)
    fault_method_code = fields.Char("Fault Method Code",help='Fault Method Code',
                                    compute="_get_fault_code",required=True)
    name = fields.Char("Fault Method Name", help='Fault Method Name', required=True)
    user_id = fields.Many2one('hr.employee', string="Create Name", default=_default_employee, required=True,
                              readonly=True)
    create_date = fields.Date("Create Date", help='Create Date', default=fields.Date.context_today, readonly=True)
    state = fields.Selection([('use', "Use"),('done', "Done")], default='use')
    active = fields.Boolean(default=True)
    remark = fields.Text("Remark", help='Remark')
    work_time = fields.Integer(string="Work Time(Minutes)")
    warranty_deadline = fields.Float(string="Warranty Deadline(Days)")
    complex_level = fields.Selection([
       ('one work', "One work"),
       ('two works', "Two works"),
       ('group works', "Group Works"),],default='one work')
    materials_control = fields.Boolean("Materials Control")
    is_important_product = fields.Boolean("Materials Control")

    # important_product = fields.Many2one('product.product',string="Important Product", domain=[('import_product', '=', True)])
    important_product_id = fields.Many2one('product.product', string="Important Product")

    reason_id = fields.Many2one('fleet_manage_fault.fault_reason',
        ondelete='cascade', string="Fault reason Name",required=True)
    appearance_id = fields.Many2one('fleet_manage_fault.fault_appearance',
        ondelete='cascade', string="Fault appearance Name")
    category_id = fields.Many2one('fleet_manage_fault.fault_category',
        ondelete='cascade', string="Fault Category Name")
    avail_ids = fields.One2many(
       'fleet_manage_fault.available_product', 'reason_id', string="Products")


    @api.multi
    def action_use(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.active = False

    @api.depends("inner_code",'reason_id.fault_reason_code')
    def _get_fault_code(self):
        for i in self:
            if i.inner_code and i.reason_id:
                i.fault_method_code = i.reason_id.fault_reason_code+i.inner_code

    @api.onchange('reason_id')
    def onchange_reason_id(self):
        if self.reason_id:
            self.category_id = self.reason_id.category_id
            self.appearance_id = self.reason_id.appearance_id

    # @api.model
    # def create(self, vals):
    #     if vals.get('reason_id'):
    #         reason = self.env['fleet_manage_fault.fault_reason'].browse(vals.get('reason_id'))
    #         if not vals['fault_method_code'].startswith(reason.fault_reason_code):
    #             vals['fault_method_code'] = reason.fault_reason_code+vals['fault_method_code']
    #     return super(FaultMethod, self).create(vals)


class AvailableProduct(models.Model):
    _name = 'fleet_manage_fault.available_product'

    product_id = fields.Many2one('product.product',string="Product")

    name = fields.Char(required=True)    
    reason_id = fields.Many2one('fleet_manage_fault.fault_method',
        ondelete='cascade', string="Fault Reason Name")
    default_dosage = fields.Integer("Default Dosage")
    max_dosage = fields.Integer("Default Dosage")
    remark = fields.Text("Remark", help="Remark")

    product_code = fields.Char("Product Code", help="Product Code")
    product_name = fields.Char("Product Name", help="Product Name")
    product_type = fields.Char("Product Type", help="Product Type")
    product_size = fields.Char("Product Size", help="Product Size")
    product_unit = fields.Char("Product Unit", help="Product Unit")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_code = self.product_id.code
            self.product_name = self.product_id.name
        else:
            self.product_code = ''
            self.product_name = ''


class FaultMaintainType(models.Model):
    """
    维修类型
    """
    _name = 'fleet_manage_fault.fault_maintain_type'

    name = fields.Char("Fault Maintain Type",require=True ,help='Fault Maintain Type')

