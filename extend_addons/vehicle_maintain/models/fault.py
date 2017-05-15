# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class FaultCategory(models.Model):
    """
    故障分类
    """
    _name = 'maintain.fault.category'
    _sql_constraints = [('code_uniq', 'unique (fault_category_code)', _("Category code already exists"))]

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    fault_category_code = fields.Char("Fault Category Code", help='Fault Category Code',required=True)
    name = fields.Char("Fault Category Name", help='Fault Category Name',required=True)
    state = fields.Selection([('use', "Use"), ('done', "Done")], default='use')
    
    active = fields.Boolean(default=True)
    appearance_ids = fields.One2many(
       'maintain.fault.appearance', 'category_id', string="appearances")
    
    reason_ids = fields.One2many(
       'maintain.fault.reason', 'category_id', string="reasons", domain=[('appearance_id','=',None)])

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
    _name = 'maintain.fault.appearance'
    _sql_constraints = [('code_uniq', 'unique (category_id, inner_code)', _("Appearance code already exists"))]

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    inner_code = fields.Char("Inner Code", help='Inner Code', required=True)
    fault_appearance_code = fields.Char("Fault appearance Code", compute="_get_fault_code",
                                        help='Fault appearance Code', required=True)
    name = fields.Char("Fault appearance Name", help='Fault appearance Name',required=True)

    state = fields.Selection([('use', "Use"),('done', "Done")], default='use')
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('maintain.fault.category', ondelete='cascade',
                                  string="Fault Category Name", required=True)
    
    reason_ids = fields.One2many(
       'maintain.fault.reason', 'appearance_id', string="Reasons")
    sequence = fields.Integer("Sequence", default=1, help="Sequence", readonly=True)

    reason_ct = fields.Integer(string="Fault Reason Count", compute='_get_reason_count')

    @api.depends("inner_code", 'category_id')
    def _get_fault_code(self):
        for i in self:
            if i.category_id and i.category_id.fault_category_code and  i.inner_code:
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
            category = self.env['maintain.fault.category'].browse(vals.get('category_id'))
            vals['sequence'] = len(category.appearance_ids)+1
        return super(FaultAppearance, self).create(vals)


class FaultReason(models.Model):
    """
    故障原因
    """
    _name = 'maintain.fault.reason'
    _sql_constraints = [('code_uniq', 'unique (category_id, appearance_id, inner_code)', _("Reason code already exists"))]

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    inner_code = fields.Char("Inner Code", help='Inner Code', required=True)
    fault_reason_code = fields.Char("Fault Reason Code",help='Fault Reason Code',
                                    compute="_get_fault_code",required=True)
    name = fields.Char("Fault Reason Name", help='Fault Reason Name',required=True)
    state = fields.Selection([('use', "Use"),('done', "Done")], default='use')
    active = fields.Boolean(default=True)
    appearance_id = fields.Many2one('maintain.fault.appearance',
                                    ondelete='cascade', string="Fault appearance Name")
    category_id = fields.Many2one('maintain.fault.category',
                                    ondelete='cascade', string="Fault Category Name", required=True)
    
    method_ids = fields.One2many('maintain.fault.method', 'reason_id', string="methods")
    sequence = fields.Integer("Sequence", help="Sequence", readonly=True)
    method_ct = fields.Integer(string="Fault Method Count", compute='_get_method_count')

    @api.depends("inner_code", 'appearance_id', 'category_id')
    def _get_fault_code(self):
        for i in self:
            if i.inner_code:
                if i.appearance_id and i.appearance_id.fault_appearance_code:
                    i.fault_reason_code = i.appearance_id.fault_appearance_code+i.inner_code
                elif i.category_id and i.category_id.fault_category_code:
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
            appearance = self.env['maintain.fault.appearance'].browse(vals.get('appearance_id'))
            vals['sequence'] = len(appearance.reason_ids) + 1
        elif vals.get('category_id',''):
            category = self.env['maintain.fault.category'].browse(vals.get('category_id'))
            vals['sequence'] = len(category.reason_ids) + 1

        return super(FaultReason, self).create(vals)


class FaultMethod(models.Model):
    """
    维修办法
    """
    _name = 'maintain.fault.method'
    _sql_constraints = [('code_uniq', 'unique (category_id, inner_code)', _("Method code already exists"))]

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    inner_code = fields.Char("Inner Code", help='Inner Code', required=True)
    fault_method_code = fields.Char("Fault Method Code",help='Fault Method Code',
                                    compute="_get_fault_code",required=True)
    name = fields.Char("Fault Method Name", help='Fault Method Name', required=True)
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

    operation_manual = fields.Text("Operation Manual", help="Operation Manual")
    inspect_standard = fields.Text("Inspect Standard", help="Inspect Standard")

    # is_important_product = fields.Boolean("Is Important Product")
    # important_product_id = fields.Many2one('product.product', string="Important Product",
    #                                        domain=[('is_important', '=', True)])


    reason_id = fields.Many2one('maintain.fault.reason',
        ondelete='cascade', string="Fault reason Name",required=True)
    appearance_id = fields.Many2one('maintain.fault.appearance',
        ondelete='cascade', string="Fault appearance Name")
    category_id = fields.Many2one('maintain.fault.category',
        ondelete='cascade', string="Fault Category Name")
    avail_ids = fields.One2many('maintain.fault.available_product', 'method_id', string="Products")


    @api.multi
    def action_use(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.active = False

    @api.depends("inner_code", 'reason_id')
    def _get_fault_code(self):
        for i in self:
            if i.inner_code and i.reason_id.fault_reason_code and i.reason_id:
                i.fault_method_code = i.reason_id.fault_reason_code+i.inner_code

    @api.onchange('reason_id')
    def onchange_reason_id(self):
        if self.reason_id:
            self.category_id = self.reason_id.category_id
            self.appearance_id = self.reason_id.appearance_id


class AvailableProduct(models.Model):
    _name = 'maintain.fault.available_product'

    # name = fields.Char(required=True)
    method_id = fields.Many2one('maintain.fault.method',
        ondelete='cascade', string="Fault Method Name")

    product_id = fields.Many2one('product.product', string="Product")
    product_code = fields.Char("Product Code", related='product_id.default_code', readonly=True)
    categ_id = fields.Many2one('product.category', related='product_id.categ_id',
                               string='Product Category', readonly=True)
    uom_id = fields.Many2one('product.uom', 'Unit of Measure', related='product_id.uom_id', readonly=True)
    onhand_qty = fields.Float('Quantity On Hand', related='product_id.qty_available', readonly=True)
    virtual_available = fields.Float('Forecast Quantity', related='product_id.virtual_available', readonly=True)

    require_trans = fields.Boolean("Require Trans", related='product_id.require_trans', readonly=True)
    vehicle_model = fields.Many2many(related='product_id.vehicle_model', relation='product_vehicle_model_rec',
                                      string='Suitable Vehicle', readonly=True)

    description = fields.Text("Product Size", related='product_id.description', readonly=True)

    change_count = fields.Integer("Change Count")
    max_count = fields.Integer("Max Count")
    remark = fields.Text("Remark", help="Remark")

    @api.constrains('change_count', 'max_count')
    def _check_change_count(self):
        for r in self:
            if r.change_count > r.max_count:
                raise exceptions.ValidationError(_("max_count must be greater than or equal to change_count"))

