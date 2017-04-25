# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import timedelta


class MaintainReport(models.Model):
    """
    车辆维修管理：报修单
    """
    _inherit = 'mail.thread'
    _name = 'maintain.report'

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    name = fields.Char(string="Report Order", help='Report Order', required=True, index=True, copy=False, default='New')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True)
    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id', store=True,
                                   readonly=True, copy=False)
    license_plate = fields.Char("License Plate", related='vehicle_id.license_plate', store=True,
                                readonly=True, copy=False)

    report_user_id = fields.Many2one('hr.employee', string="Report Name", default=_default_employee, required=True)
    create_name = fields.Many2one('hr.employee', string="Create Name", default=_default_employee, required=True,
                                  readonly=True)

    department = fields.Many2one('hr.department', string="Department", related='create_name.department_id',
                                 readonly=True)

    report_date = fields.Date('Report Date',help='Report Date',default=fields.Date.context_today)
    repair_category = fields.Selection([('normal repair', "normal repair"),
                                        ('anchor repair', "anchor repair"),
                                        ('accident repair', "accident repair"),
                                        ('maintain repair', 'maintain repair')],
                                       string='repair category', default='normal repair')
    repair_level = fields.Char(string="Repair Level")
    is_fault_vehicle = fields.Boolean("Is Fault Vehicle", default=True)

    state = fields.Selection([
                            # ('back', "Back"),
                            ('draft', "Draft"),
                            ('precheck', "Precheck"),
                            ('dispatch', "Dispatch"),
                            ('wait_repair',"Wait Repair"),
                            ('repair', "Repair"),
                            ('inspect', "Inspect"),
                            ('completed', "Completed")], default='draft')
    repair_ids = fields.One2many("maintain.repair", 'report_id', string='Maintain Repair',
                                 states={'completed':[('readonly', True)],
                                         # 'repair':[('readonly', True)]
                                         }
    )

    partner_id = fields.Many2one('hr.department', string="Partner", related='create_name.department_id')
    fleet = fields.Char(string="Fleet")
    repair_plant = fields.Char(string="Repair Plant")
    remark = fields.Text(string="Remark")
    dispatch_count = fields.Integer("Dispatch Count",compute="_get_dispatch_count")

    def _get_dispatch_count(self):
        """
        功能：计算待派工的维修单
        """
        repair = self.env['maintain.repair'].search([("report_id", '=', self.id), ('state', '=', 'dispatch')])
        self.dispatch_count = len(repair)

    @api.multi
    def action_to_open(self):
        """
        报修单:
            功能：跳转到派工状态的维修单
        """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('vehicle_maintain', xml_id)
            res.update(
                context=dict(self.env.context, default_report_id=self.id),
                domain=[('report_id', '=', self.id), ('state', '=', 'dispatch')]
            )
            return res
        return False

    @api.model
    def create(self, data):
        """
        报修单:
            功能：自动生成订单号：前缀BXD+序号
        """
        if data.get('name', 'New') == 'New':
            data['name'] = self.env['ir.sequence'].next_by_code('maintain.report') or '/'
        report = super(MaintainReport, self.with_context(mail_create_nolog=True)).create(data)
        report.message_post(body=_('%s has been added to the report!') % (report.name,))
        return report

    @api.multi
    def action_submit_precheck(self):    #
        """
        报修单:
            功能：提交检验
            状态：草稿->预检
        """
        self.ensure_one()
        if not self.repair_ids:
            raise exceptions.UserError(_("Maintain Repair Required!"))
        else:
            self.state = 'precheck'
            for i in self.repair_ids:
                if i.state == 'draft':
                    i.state = 'precheck'

    @api.multi
    def action_precheck_to_draft(self):
        """
        预检单:
            功能：检验退回
            状态：预检->草稿
        """
        self.write({"state": 'draft'})

    @api.multi
    def action_repair_to_precheck(self):
        """
        预检单:
            功能：退回检验
            状态：维修->预检
        """
        self.write({"state": 'precheck'})

    @api.multi
    def action_precheck_to_repair(self):
        """
        预检单:
            功能：预检通过
            状态：预检->维修
        """
        self.ensure_one()
        def _default_employee(self):
            emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
            return emp_ids and emp_ids[0] or False

        report_user_id = self._default_employee()
        self.state = 'repair'
        for i in self.repair_ids:
            if i.state == 'precheck':
                i.state = 'dispatch'

class MaintainRepair(models.Model):
    """
    车辆维修管理：维修单
    """
    _inherit = 'mail.thread'
    _name = 'maintain.repair'

    name = fields.Char(string="Repair Order", help='Repair Order', required=True, index=True,
                       copy=False, default='New', readonly=True)
    report_id = fields.Many2one("maintain.report", ondelete='cascade',
                                string="Report Order", required=True, readonly=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No',
                                 related='report_id.vehicle_id', store=True, readonly=True, copy=False)
    vehicle_type = fields.Many2one("fleet.vehicle.model", related='report_id.vehicle_id.model_id',
                                   store=True, readonly=True, copy=False)
    license_plate = fields.Char(string="License Plate", help='License Plate',
                                related='report_id.vehicle_id.license_plate', store=True, readonly=True, copy=False)
    repair_category = fields.Selection(string="repair category", help='repair category',
                                   related='report_id.repair_category', store=True, readonly=True, copy=False)

    fault_category_id = fields.Many2one("maintain.fault.category", ondelete='set null', string="Fault Category",
                                        required=True, states={
                                          'completed': [('readonly', True)],
                                          'inspect': [('readonly', True)],
                                          'repair': [('readonly', True)],
                                        })
    fault_appearance_id = fields.Many2one("maintain.fault.appearance", ondelete='set null',
                                          string="Fault Appearance", states={
                                          'completed': [('readonly', True)],
                                          'inspect': [('readonly', True)],
                                          'repair': [('readonly', True)],
                                        })
    fault_reason_id = fields.Many2one("maintain.fault.reason", ondelete='set null',
                                      string="Fault Reason", states={
                                          'completed': [('readonly', True)],
                                          'inspect': [('readonly', True)],
                                          'repair': [('readonly', True)],
                                        })
    fault_method_id = fields.Many2one("maintain.fault.method", ondelete='set null',
                                      string="Fault Method", states={
                                          'completed': [('readonly', True)],
                                          'inspect': [('readonly', True)],
                                          'repair': [('readonly', True)],
                                        })
    fault_method_code = fields.Char(related='fault_method_id.fault_method_code', store=True, readonly=True, copy=False)
    work_time = fields.Integer(related='fault_method_id.work_time', store=True, readonly=True, copy=False)
    materials_control = fields.Boolean("Materials Control", readonly=True, copy=False)

    plan_start_time = fields.Datetime("Plan Start Time", help="Plan Start Time")
    plan_end_time = fields.Datetime("Plan End Time", help="Plan End Time", compute='_get_end_datetime')
    real_start_time = fields.Datetime("Real Start Time", help="Real Start Time")
    real_end_time = fields.Datetime("Real End Time", help="Real End Time")
    user_id = fields.Many2one('hr.employee', string="Repair Name")

    repair_names = fields.Char(string='Repair Names', help="Repair Names", compute='_get_repair_names')
    state = fields.Selection([
        ('draft', "Draft"),
        ('precheck', "Precheck"),
        ('dispatch', "Dispatch"),
        ('wait_repair', "Wait Repair"),
        ('repair', "Repair"),
        ('inspect', "Inspect"),
        ('completed', "Completed")], default='draft', readonly=True)

    job_ids = fields.One2many("maintain.repair_jobs", 'repair_id', string='Maintain Repair Jobs',
                              states={
                                  'completed': [('readonly', True)],
                                  'inspect': [('readonly', True)],
                                  'repair': [('readonly', True)],
                              })

    percentage_work = fields.Float(help='percentage_work', digits=(2, 1))

    available_product_ids = fields.One2many("maintain.available_product", 'repair_id',
                                            string='Available Product')
    operation_manual = fields.Text("Operation Manual", related='fault_method_id.operation_manual',
                                   help="Operation Manual",store=True, readonly=True, copy=False)
    inspect_standard = fields.Text("Inspect Standard", related='fault_method_id.inspect_standard',
                                   help="Inspect Standard",store=True, readonly=True, copy=False)

    repair_type = fields.Selection([('vehicle_repair',"vehicle_repair"),
                                    ('assembly_repair',"assembly_repair")],
                                   default='vehicle_repair', string="Repair Type")

    picking_ids = fields.One2many("stock.picking", 'repair_id', string='Stock Pickings')


    @api.depends('plan_start_time', 'work_time')
    def _get_end_datetime(self):
        """
        维修单:
           功能：计算计划结束时间
        """
        for r in self:
            if not (r.plan_start_time and r.work_time):
                continue
            start = fields.Datetime.from_string(r.plan_start_time)
            r.plan_end_time = start + timedelta(seconds=r.work_time*60)

    @api.multi
    def write(self, vals):
        if "fault_method_id" in vals and vals.get('fault_method_id'):
            for i in self.available_product_ids:  # 维修单存在物料清单，要删除
                i.unlink()
            datas = []
            method = self.env['maintain.fault.method'].browse(vals.get('fault_method_id'))
            if method.materials_control:
                for j in method.avail_ids:
                    data = {
                        'repair_id': j.id,
                        'method_id': j.method_id.id,
                        'product_id': j.product_id.id,
                        'change_count': j.change_count,
                        'max_count': j.max_count,
                        'require_trans': j.require_trans,
                    }
                    datas.append((0, 0, data))
            vals.update({'available_product_ids': datas, 'materials_control':method.materials_control})
        return super(MaintainRepair, self).write(vals)

    @api.onchange('percentage_work')
    def _verify_percentage_work(self):
        """
        维修单:
           功能：验证百分比的大小 不能小于0或者大于100
        """
        if self.percentage_work < 0 or self.percentage_work > 100:
            return {
                'warning': {
                    'title': "Incorrect 'percentage_work' value",
                    'message': "The number of available percentage_work may not be negative",
                }
            }

    @api.onchange('fault_appearance_id')
    def onchange_appearance_id(self):
        if self.fault_appearance_id:
            self.fault_category_id = self.fault_appearance_id.category_id

    @api.onchange('fault_method_id')
    def onchange_method_id(self):
        if self.fault_method_id:
            self.fault_reason_id = self.fault_method_id.reason_id
            self.materials_control = self.fault_method_id.materials_control
            if self.fault_method_id.reason_id.appearance_id:
                self.fault_appearance_id = self.fault_method_id.reason_id.appearance_id
                self.fault_category_id = self.fault_method_id.reason_id.appearance_id.category_id
            else:
                self.fault_category_id = self.fault_method_id.reason_id.category_id
                self.fault_appearance_id = None

    @api.model
    def create(self, vals):
        """
        维修单:
            自动生成订单号：前缀WXD+序号
        """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintain.repair') or '/'
        return super(MaintainRepair, self).create(vals)

    @api.multi
    def dispatch(self):
        """
        维修单:
            派工
                功能：1判断工时比例是否已经超过100
                    2.增加工时管理记录
                状态：派工->待修
        """
        self.ensure_one()
        if not self.user_id:
            raise exceptions.UserError(_("Maintain Repair Names Required!"))
        if not self.plan_start_time:
            raise exceptions.UserError(_("Maintain Repair StartTime Required!"))
        percentage_work = sum(i.percentage_work for i in self.job_ids)
        if percentage_work + self.percentage_work > 100:
            raise exceptions.UserError(_("Dispatching the proportion of more than 100"))
        self.state = 'wait_repair'
        vals = {
            "fault_category_id": self.fault_category_id.id,
            "fault_appearance_id": self.fault_appearance_id.id or None,
            "fault_reason_id": self.fault_reason_id.id,
            "fault_method_id": self.fault_method_id.id,
            "plan_start_time": self.plan_start_time,
            "plan_end_time": self.plan_end_time,
            "work_time": self.work_time,
            "percentage_work": self.percentage_work,
            "user_id": self.user_id.id,
            "sequence": len(self.job_ids)+1
        }
        self.write({
            'percentage_work': False,
            "user_id": False,
            'plan_start_time': False,
            'state': 'wait_repair',
            'job_ids': [(0, 0, vals)]
        })

    @api.depends("job_ids")
    def _get_repair_names(self):
        """
        维修单:
            功能：获取维修人名字
        """
        for i in self:
            repair_names = set()
            for j in i.job_ids:
                repair_names.add(j.user_id.name)
            i.repair_names = ",".join(list(repair_names))

    @api.multi
    def action_start_repair(self):
        """
        维修单:
            功能：开工
            状态：待修->维修
            更新工时管理的实际开工时间
        """
        self.ensure_one()
        if not self.job_ids:
            raise exceptions.UserError(_("Maintain Repair Jobs Required!"))
        self.write({'state': 'repair'})

        for i in self.job_ids:
            i.real_start_time = fields.Datetime.now()
        if self.materials_control:
            avail_products = self.mapped('available_product_ids').filtered(lambda x: x.change_count > 0)
            picking_type = self.env.ref('stock_picking_types.picking_type_issuance_of_material')
            location_id = self.env.ref('stock.stock_location_stock').id     # 库存
            location_dest_id = self.env.ref('stock_picking_types.stock_location_ullage').id  #维修(生产)虚位

            for products in [avail_products]:
                if not products:
                    continue
                move_lines = []
                picking = []
                for i in products:
                    vals = {
                        'name': 'stock_move_repair',
                        'product_id': i.product_id.id,
                        'product_uom': i.product_id.uom_id.id,
                        'product_uom_qty': i.change_count,
                    }
                    move_lines.append((0, 0, vals))
                if move_lines:
                    picking = self.env['stock.picking'].create({
                        'origin': self.name,
                        'location_id': location_id,
                        'location_dest_id': location_dest_id,
                        'picking_type_id': picking_type.id,
                        'repair_id': self.id,
                        'move_lines': move_lines
                    })
                if picking:
                    picking.action_confirm()



    @api.multi
    def action_start_inspect(self):
        """
        维修单:
            功能：报检
            状态：维修->检验
            更新检验单的报检时间
            更新工时管理的实际完工时间
        """
        self.write({
            'state': 'inspect',
            'start_inspect_time': fields.Datetime.now()
        })
        for i in self.job_ids:
            i.real_end_time = fields.Datetime.now()

    @api.multi
    def create_get_picking(self):
        """
        创建领料单
        """
        self.ensure_one()
        context = dict(self.env.context,
                       default_repair_id=self.id,
                       default_origin=self.name,
                       default_picking_type_id=self.env.ref('stock_picking_types.picking_type_picking_material').id,
                       )
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'res_id': '',
            'context': context
        }

    @api.multi
    def create_back_picking(self):
        """
        创建退料单
        """
        self.ensure_one()
        context = dict(self.env.context,
                       default_repair_id=self.id,
                       default_origin=self.name,
                       default_picking_type_id=self.env.ref('stock_picking_types.picking_type_return_material').id,
                       )
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'res_id': '',
            'context': context
        }


class MaintainAvailableProduct(models.Model):
    _name = 'maintain.available_product'

    repair_id = fields.Many2one('maintain.repair',
                                ondelete='cascade', string="Repair")
    method_id = fields.Many2one('maintain.fault.method',
                                ondelete='set null', string="Fault Method Name")

    product_id = fields.Many2one('product.product', string="Product")
    product_code = fields.Char("Product Code", related='product_id.default_code')
    categ_id = fields.Many2one('product.category', related='product_id.categ_id',
                               string='Product Category')
    uom_id = fields.Many2one('product.uom', 'Unit of Measure', related='product_id.uom_id')
    onhand_qty = fields.Float('Quantity On Hand', related='product_id.qty_available')
    virtual_available = fields.Float('Forecast Quantity', related='product_id.virtual_available')
    require_trans = fields.Boolean("Require Trans", readonly=True)
    vehicle_model = fields.Many2many(related='product_id.vehicle_model', relation='product_vehicle_model_rec',
                                      string='Suitable Vehicle', readonly=True)
    product_size = fields.Text("Product Size", related='product_id.description', readonly=True)

    change_count = fields.Integer("Change Count")
    max_count = fields.Integer("Max Count")


class MaintainRepairJobs(models.Model):
    """
    车辆维修管理：维修单工时管理
    """
    _name = 'maintain.repair_jobs'
    name = fields.Char("Job Name", help="Job Name")
    sequence = fields.Integer("Sequence", help="Sequence")
    repair_id = fields.Many2one("maintain.repair", ondelete='cascade',
                                string="Maintain Repair")
    fault_category_id = fields.Many2one("maintain.fault.category", ondelete='set null',
                                        string="Fault Category")
    fault_appearance_id = fields.Many2one("maintain.fault.appearance", ondelete='set null',
                                          string="Fault Appearance")
    fault_reason_id = fields.Many2one("maintain.fault.reason", ondelete='set null', string="Fault Reason")
    fault_method_id = fields.Many2one("maintain.fault.method", ondelete='set null', string="Fault Method")
    user_id = fields.Many2one('hr.employee', string="Repair Name", required=True)
    plan_start_time = fields.Datetime("Plan Start Time", help="Plan Start Time")
    plan_end_time = fields.Datetime("Plan End Time", help="Plan End Time")
    real_start_time = fields.Datetime("Real Start Time", help="Real Start Time")
    real_end_time = fields.Datetime("Real End Time", help="Real End Time")
    percentage_work = fields.Float('Percentage Work', help='Percentage Work')

    work_time = fields.Float('Work Time', help='Work Time')
    my_work = fields.Float('My Work', help='My Work', compute="_get_my_work")
    real_work = fields.Float('Real Work', help='Real Work', compute="_get_real_work")

    @api.depends('real_start_time', 'real_end_time')
    def _get_real_work(self):
        for i in self:
            if i.real_start_time and i.real_end_time:
                start_time = fields.Datetime.from_string(i.real_start_time)
                end_time = fields.Datetime.from_string(i.real_end_time)
                i.real_work = (end_time-start_time).seconds/60.0

    @api.depends('plan_start_time', 'plan_end_time','percentage_work',)
    def _get_my_work(self):
        for i in self:
            if i.plan_start_time and i.plan_end_time:
                start_time = fields.Datetime.from_string(i.plan_start_time)
                end_time = fields.Datetime.from_string(i.plan_end_time)
                work_time = (end_time - start_time).seconds / 60.0
                i.my_work = work_time * i.percentage_work/100


class MaintainInspect(models.Model):
    """
    车辆维修管理：检验单
    """
    # _name = 'maintain.maintain_inspect'
    _inherit = 'maintain.repair'

    inspect_result = fields.Selection([('qualified', 'Qualified'),
                                       ('defective','Defective')], string="Inspect Result")

    start_inspect_time = fields.Datetime("Start Inspect Time")
    end_inspect_time = fields.Datetime("End Inspect Time")
    return_record_ids = fields.One2many("maintain.return_record", 'repair_id', string='Maintain Repair')

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False
    inspect_user_id = fields.Many2one('hr.employee', string="Inspect Name", default=_default_employee, required=True)
    rework_count = fields.Integer("Rework Count", compute="_get_rework_count")

    def _get_rework_count(self):
        """
        检验单:
            功能：获取退检次数
        """
        for i in self:
            i.rework_count = len(i.return_record_ids)

    @api.multi
    def action_completed(self):
        """
        检验单:
            功能：检验通过(批量检查通过)
            状态：检验->完工
            更新检验单的检验时间和检验结论
            判断该检验单对应的报修单是否完工
        """
        for i in self:
            if i.state not in ('inspect', 'completed'):
                raise exceptions.UserError(_("Selected inspect(s) cannot be confirmed as they are not in 'inspect' state"))
            i.state = 'completed'
            i.inspect_result = 'qualified'
            i.end_inspect_time = fields.Datetime.now()

            if all(repair.state in ['completed'] for repair in i.report_id.repair_ids):
                i.report_id.state = 'completed'

    @api.multi
    def action_return(self, reason=''):
        """
        检验单:
            功能：检验退回
            状态：检验->维修
            更新检验单的检验时间和检验结论
            判断该检验单对应的报修单是否完工
        """
        inspect_return_time = fields.Datetime.now()
        vals = {
            "repair_id": self.id,
            "inspect_return_time": inspect_return_time,
            "return_reason": reason,
            "sequence": len(self.return_record_ids) + 1
        }
        self.write({
            "state":'repair',
            "end_inspect_time": inspect_return_time,
            "inspect_result": "defective",
            "return_record_ids": [(0, 0, vals)]
        })


class MaintainReturnRecord(models.Model):
    """
    退检记录
    """
    _name = 'maintain.return_record'
    repair_id = fields.Many2one('maintain.repair', string="Repair Order",
                                required=True, readonly=True)
    inspect_user_id = fields.Many2one('hr.employee', related='repair_id.inspect_user_id', string="Inspect Name",
                                      required=True, readonly=True)
    repair_names = fields.Char(string='Repair Names',related='repair_id.repair_names')
    fault_method_id = fields.Many2one("maintain.fault.method", related='repair_id.fault_method_id',
                                      ondelete='set null', string="Fault Method")
    return_reason = fields.Text("Return Reason")
    inspect_return_time = fields.Datetime("Inspect Return Time")
    sequence = fields.Integer("Sequence")
