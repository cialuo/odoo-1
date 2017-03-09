# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FleetMaintainReport(models.Model):
    """
    车辆维修管理：报修单
    """
    _name = 'fleet_manage_maintain.maintain_report'
    name = fields.Char(string="Report Bill", help='Report Bill', required=True, index=True, copy=False, default='New')
    vehicle_no = fields.Char(string="Vehicle No", help='Vehicle No')
    vehicle_type = fields.Char(string="Vehicle Type", help='Vehicle Type')
    user_id = fields.Many2one('res.users', string="Report Name")
    report_date = fields.Date(help='Report Date')

    repair_type = fields.Selection([
       ('type1', "type1"),
       ('type2', "type2"),
       ('type3', "type3"),
       ])
    repair_level = fields.Selection([
       ('level1', "level1"),
       ('level2', "level2"),
       ('level3', "level3"),
       ])
    is_fault_vehicle = fields.Boolean("Is Fault Vehicle", default=True)

    state = fields.Selection(
           selection=[('back', "Back"),
            ('draft', "Draft"),
            ('precheck', "Precheck"),
            ('dispatch', "Dispatch"),
            ('repair', "Repair"),
            ('inspect', "Inspect"),
            ('done', "Done")], default='draft')
    repair_ids = fields.One2many("fleet_manage_maintain.maintain_repair", 'report_id',string='Maintain Repair')
    partner_id = fields.Many2one('res.partner', string="Repair Company")
    fleet = fields.Char(string="Fleet")
    repair_plant = fields.Char(string="Repair Plant")
    create_name = fields.Many2one('res.users', string="Create Name")
    create_name_company = fields.Char(string="Create Name Company")
    remark = fields.Text(string="Remark")
    dispatch_count = fields.Integer("Dispatch Count",compute="_get_dispatch_count")

    def _get_dispatch_count(self):  #计算待派工的维修单
        repair = self.env['fleet_manage_maintain.maintain_repair'].search([("report_id", '=', self.id),('state','=','dispatch')])
        self.dispatch_count = len(repair)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet_manage_maintain.maintain_report') or '/'
        return super(FleetMaintainReport, self).create(vals)

    @api.multi
    def action_back(self): #检验退回
        self.state = 'back'

    @api.multi
    def action_draft(self): #设为草稿
        self.state = 'draft'

    @api.multi
    def action_precheck(self): #提交检验 或者退回检验
        self.state = 'precheck'

    @api.multi
    def action_repair(self): #批量派工
        self.state = 'repair'

    @api.multi
    def action_inspect(self):  #维修完成
        self.state = 'inspect'

    @api.multi
    def action_dispatch(self):  #预检通过并创建交接单  或者重新派工
        self.state = 'dispatch'
        self.ensure_one()
        vals = {
            "report_id": self.id,
            # "fault_appearance_id": self.partner_id.id,
        }
        deliverys = self.env['fleet_manage_maintain.maintain_delivery'].search([("report_id", '=', self.id)])
        if not deliverys:
            self.env['fleet_manage_maintain.maintain_delivery'].create(vals)


    @api.multi
    def delivery_manage(self):  #跳转到交接单
        self.ensure_one()
        deliverys = self.env['fleet_manage_maintain.maintain_delivery'].search([("report_id",'=',self.id)])
        action = self.env.ref('fleet_manage_maintain.fleet_manage_maintain_delivery_action').read()[0]
        action['res_id'] = deliverys.id#[('id', '=', deliverys.id)]
        action['views'] = [(self.env.ref('fleet_manage_maintain.fleet_manage_delivery_view_form').id, 'form')]
        return action


class FleetMaintainRepair(models.Model):
    """
    车辆维修管理：维修单
    """
    _name = 'fleet_manage_maintain.maintain_repair'
    name = fields.Char(string="Repair Bill", help='Repair Bill', required=True, index=True, copy=False, default='New')
    report_id = fields.Many2one("fleet_manage_maintain.maintain_report",ondelete='cascade',string="Report Code")
    vehicle_no = fields.Char(string="Vehicle No", help='Vehicle No')
    vehicle_type = fields.Char(string="Vehicle Type", help='Vehicle Type')
    vehicle_license = fields.Char(string="Vehicle License", help='Vehicle License')

    guarantee_level = fields.Char(string="Guarantee Level", help='Guarantee Level')

    fault_category_id = fields.Many2one("fleet_manage_fault.fault_category", ondelete='set null', string="Fault Category")
    fault_appearance_id = fields.Many2one("fleet_manage_fault.fault_appearance", ondelete='set null', string="Fault Appearance")
    fault_reason_id = fields.Many2one("fleet_manage_fault.fault_reason", ondelete='set null', string="Fault Reason")
    fault_method_id = fields.Many2one("fleet_manage_fault.fault_method", ondelete='set null', string="Fault Method")

    plan_start_time = fields.Datetime("Plan Start Time", help="Plan Start Time")
    plan_end_time = fields.Datetime("Plan End Time", help="Plan End Time")

    real_start_time = fields.Datetime("Real Start Time", help="Real Start Time")
    real_end_time = fields.Datetime("Real End Time", help="Real End Time")

    user_id = fields.Many2one('res.users', string="Repair Name")
    repair_names = fields.Char(string='Repair Names', help="Repair Names",compute='_get_repair_names')
    state = fields.Selection([
        ('dispatch', "Dispatch"),
        ('repair', "Repair"),
        ('inspect', "Inspect"),
        ('done', "Done"),],default='dispatch', readonly=True)

    job_ids = fields.One2many("fleet_manage_maintain.maintain_repair_jobs", 'repair_id', string='Maintain Repair Jobs')
    standard_work = fields.Float(help='standard_work')
    percentage_work = fields.Float(help='percentage_work')

    available_product_ids = fields.One2many("fleet_manage_maintain.available_product", 'repair_id', string='Available Product')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet_manage_maintain.maintain_repair') or '/'
        return super(FleetMaintainRepair, self).create(vals)

    @api.multi
    def action_repair(self):  #开工
        self.state = 'repair'

    @api.multi
    def action_inspect(self):  #报检
        self.state = 'inspect'
        self.inspect_time = fields.Datetime.now()

    @api.multi
    def dispatch(self):         #派工
        # self.env['fleet_manage_maintain.maintain_repair_jobs'].create()
        self.ensure_one()
        vals = {
            # "repair_id": self.id,
            "fault_category_id": self.fault_category_id.id,
            "fault_appearance_id": self.fault_appearance_id.id,
            "fault_reason_id": self.fault_reason_id.id,
            "fault_method_id": self.fault_method_id.id,
            "plan_start_time": self.plan_start_time,
            "plan_end_time": self.plan_end_time,
            "standard_work": self.standard_work,
            "percentage_work": self.percentage_work,
            "user_id":self.user_id.id,
            "sequence":len(self.job_ids)+1
        }
        self.write({'job_ids': [(0, 0, vals)]})

    @api.depends("job_ids")
    def _get_repair_names(self):  #获取维修人名字
        for i in self:
            repair_names = set()
            for j in i.job_ids:
                repair_names.add(j.user_id.name)
            repair_names = ",".join(list(repair_names))

            i.repair_names = repair_names


class FleetMaintainAvailableProduct(models.Model):
    _name = 'fleet_manage_maintain.available_product'

    product_id = fields.Many2one('product.product',string="Product")
    # name = fields.Char(required=True)
    repair_id = fields.Many2one('fleet_manage_maintain.maintain_repair',
        ondelete='set null', string="Repair")


    product_code = fields.Char("Product Code", help="Product Code")
    product_name = fields.Char("Product Name", help="Product Name")
    max_available_count = fields.Integer("Max Available Count", help="Max Available Count")
    default_avail_count = fields.Integer("Default Available Count", help="Default Available Count")
    stock_count = fields.Integer("Stock Count", help="Stock Count")
    available_count = fields.Integer("Available Count", help="Available Count")

    post_old_get_new = fields.Boolean("Post Old Get New")
    meet_vehicle_type = fields.Char("Meet Vehicle Type", help="Meet Vehicle Type")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_code = self.product_id.code
            self.product_name = self.product_id.name



class FleetMaintainRepairJobs(models.Model):
    """
    车辆维修管理：维修单工时管理
    """
    _name = 'fleet_manage_maintain.maintain_repair_jobs'
    name = fields.Char("Inspect Bill", help="Inspect Bill")
    sequence = fields.Integer("Sequence", help="Sequence")
    repair_id = fields.Many2one("fleet_manage_maintain.maintain_repair", ondelete='set null',
                                        string="Maintain Repair")
    fault_category_id = fields.Many2one("fleet_manage_fault.fault_category", ondelete='set null',
                                        string="Fault Category")
    fault_appearance_id = fields.Many2one("fleet_manage_fault.fault_appearance", ondelete='set null',
                                          string="Fault Appearance")
    fault_reason_id = fields.Many2one("fleet_manage_fault.fault_reason", ondelete='set null', string="Fault Reason")
    fault_method_id = fields.Many2one("fleet_manage_fault.fault_method", ondelete='set null', string="Fault Method")
    user_id = fields.Many2one('res.users', string="Repair Name")
    plan_start_time = fields.Datetime("Plan Start Time", help="Plan Start Time")
    plan_end_time = fields.Datetime("Plan End Time", help="Plan End Time")
    real_start_time = fields.Datetime("Real Start Time", help="Real Start Time")
    real_end_time = fields.Datetime("Real End Time", help="Real End Time")
    standard_work = fields.Float(help='standard_work')
    my_work = fields.Float(help='my_work')
    real_work = fields.Float(help='real_work')
    percentage_work = fields.Float(help='percentage_work')


class FleetMaintainDelivery(models.Model):
    """
    车辆维修管理：交接单
    """
    _name = 'fleet_manage_maintain.maintain_delivery'
    name = fields.Char(string="Delivery Bill", help='Delivery Bill', required=True, index=True, copy=False, default='New')
    report_id = fields.Many2one("fleet_manage_maintain.maintain_report", ondelete='cascade', string="Report Code")
    vehicle_no = fields.Char(string="Vehicle No", help='Vehicle No')
    vehicle_type = fields.Char(string="Vehicle Type", help='Vehicle Type')
    vehicle_license = fields.Char(string="Vehicle License", help='Vehicle License')
    delivery_time = fields.Datetime("Delivery Time", help="Delivery Time")
    delivery_return_time = fields.Datetime("Delivery Return Time", help="Delivery Return Time")

    state = fields.Selection([
        ('draft', "Draft"),
        ('delivery', "Delivery"),
        ('return', "Return"),],default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet_manage_maintain.maintain_delivery') or '/'
        return super(FleetMaintainDelivery, self).create(vals)

    @api.multi
    def action_delivery(self):
        self.state = 'delivery'
        self.delivery_time = fields.Datetime.now()

    @api.multi
    def action_return(self):
        self.state = 'return'
        self.delivery_return_time = fields.Datetime.now()




class FleetMaintainInspect(models.Model):
    """
    车辆维修管理：检验单
    """
    # _name = 'fleet_manage_maintain.maintain_inspect'
    _inherit = 'fleet_manage_maintain.maintain_repair'
    #name = fields.Char("Inspect Bill", help="Inspect Bill")
    inspect_result = fields.Char("Inspect Result", help="Inspect Result")
    rework_count = fields.Integer("Rework Count",help="Rework Count")
    inspect_time = fields.Datetime("Inspect Time", help="Inspect Time")
    inspect_standard = fields.Text("Inspect Standard", help="Inspect Standard")

    @api.multi
    def action_done(self):
        self.state = 'done'
