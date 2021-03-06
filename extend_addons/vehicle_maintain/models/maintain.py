# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime
from datetime import timedelta
import time

import odoo.addons.decimal_precision as dp


class MaintainReport(models.Model):
    """
    车辆维修管理：报修单
    """
    _inherit = 'mail.thread'
    _name = 'maintain.manage.report'
    _order = "id desc"

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    name = fields.Char(string="Report Order", help='Report Order', required=True, index=True, copy=False, default='/')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True,
                                domain="[('vehicle_life_state', '=', 'operation_period'),('state', '=', 'normal')]")
    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id', store=True,
                                   readonly=True, copy=False, string="Vehicle Model")
    license_plate = fields.Char("License Plate", related='vehicle_id.license_plate', store=True,
                                readonly=True, copy=False)

    report_user_id = fields.Many2one('hr.employee', string="Report Name", default=_default_employee, required=True)
    report_date = fields.Date('Report Date', help='Report Date', default=fields.Date.context_today)

    repair_category = fields.Selection([('normal repair', "normal repair"),
                                        ('anchor repair', "anchor repair"),
                                        ('accident repair', "accident repair"),
                                        ('maintain repair', 'maintain repair')],
                                       string='repair category', default='normal repair')

    repair_level = fields.Char(string="Repair Level")
    is_fault_vehicle = fields.Boolean("Is Fault Vehicle", default=True)

    state = fields.Selection([
                            ('discard', "discard"),
                            ('draft', "Draft"),
                            ('precheck', "Precheck"),
                            ('dispatch', "Dispatch"),
                            ('wait_repair',"Wait Repair"),
                            ('repair', "Repair"),
                            ('inspect', "Inspect"),
                            ('completed', "Completed")], default='draft', string="Report State")
    repair_ids = fields.One2many("maintain.manage.repair", 'report_id', string='Maintain Repair',
                                 states={'completed':[('readonly', True)],
                                         'repair':[('readonly', True)]
                                         }
    )

    create_name = fields.Many2one('hr.employee', string="Create Name", default=_default_employee, required=True,
                                  readonly=True)

    create_name_department = fields.Many2one('hr.department', string="Create Name Department",
                                             related='create_name.department_id', readonly=True)

    report_company_id = fields.Many2one('res.company', related='vehicle_id.company_id', string="Report Company",
                                        required=True, store=True)#报修公司
    repair_company_id = fields.Many2one('res.company', string="Repair Company")#承修公司

    repair_plant_id = fields.Many2one('vehicle.plant', string="Repair Plant")  # 维修厂 (承修车间)

    # 修理厂所属部门
    depa_id = fields.Many2one('hr.department', related='repair_plant_id.department_id',
                              store=True, readonly=True)

    remark = fields.Text(string="Remark")

    dispatch_count = fields.Integer("Dispatch Count", compute="_get_dispatch_count")

    #2017年7月25日 新增字段：预检时间；用于计算抢修总时长
    preflight_date = fields.Datetime(string='Preflight date')


    @api.multi
    def unlink(self):
        """
        控制单据的删除，只能删除草稿状态的单据
        :return:
        """
        for order in self:
            if not order.state == 'draft':
                raise exceptions.UserError(_('In order to delete a report order, you must set it draft first.'))

        return super(MaintainReport, self).unlink()

    def _get_dispatch_count(self):
        """
        功能：计算待派工的维修单
        """
        repair = self.env['maintain.manage.repair'].search([("report_id", '=', self.id), ('state', '=', 'dispatch')])
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
        if data.get('name', '/') == '/':
            data['name'] = self.env['ir.sequence'].next_by_code('maintain.manage.report') or '/'
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

    @api.multi
    def action_precheck_to_discard(self):
        """
        预检单:
            功能：检验退回
            状态：预检->作废
        """
        self.write({"state": 'discard'})

    @api.multi
    def action_repair_to_precheck(self):
        """
        预检单:
            功能：退回检验
            状态：维修->预检
        """
        self.write({"state": 'precheck'})
        self.vehicle_id.state = 'normal'

    @api.multi
    def action_precheck_to_repair(self):
        """
        预检单:
            功能：预检通过
            状态：预检->维修
            修改车辆状态 -> 抢修
        """
        self.ensure_one()
        self.write({
                "state": 'repair',
                "preflight_date": fields.Datetime.now()} #2017年7月25日 记录预检通过时间
                )
        self.vehicle_id.state = 'repair'

        for i in self.repair_ids:
            if i.state in ('draft'):
                i.state = 'wait_dispatch'


class MaintainRepair(models.Model):
    """
    车辆维修管理：维修单
    """
    _inherit = 'mail.thread'
    _name = 'maintain.manage.repair'
    _order = "id desc"

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    name = fields.Char(string="Repair Order", help='Repair Order', required=True, index=True, default='/', readonly=True)
    report_id = fields.Many2one("maintain.manage.report", ondelete='cascade',
                                string="Report Order", required=True, readonly=True)

    report_company_id = fields.Many2one('res.company', related='report_id.report_company_id', string="Report Company",
                                        required=True)         #报修公司
    repair_company_id = fields.Many2one('res.company', related='report_id.repair_company_id', store=True,
                                        string="Repair Company")#承修公司

    # 修理厂所属部门
    depa_id = fields.Many2one('hr.department', related='report_id.depa_id',
                              store=True, readonly=True)

    report_user_id = fields.Many2one('hr.employee', string="Report Name", related='report_id.report_user_id')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No',
                                 related='report_id.vehicle_id', store=True, readonly=True)
    vehicle_type = fields.Many2one("fleet.vehicle.model", related='report_id.vehicle_id.model_id',
                                   store=True, readonly=True, string="Vehicle Model")
    license_plate = fields.Char(string="License Plate", help='License Plate',
                                related='report_id.vehicle_id.license_plate', store=True, readonly=True)
    repair_category = fields.Selection(string="repair category", help='repair category',
                                       related='report_id.repair_category', store=True, readonly=True)
    fault_category_id = fields.Many2one("maintain.fault.category", ondelete='set null', string="Fault Category",
                                        required=True, states={
                                          'completed': [('readonly', True)],
                                          'inspect': [('readonly', True)],
                                        })
    fault_appearance_id = fields.Many2one("maintain.fault.appearance", ondelete='set null',
                                          string="Fault Appearance", states={
                                              'completed': [('readonly', True)],
                                              'inspect': [('readonly', True)],
                                        })
    fault_reason_id = fields.Many2one("maintain.fault.reason", ondelete='set null',
                                      string="Fault Reason", states={
                                          'completed': [('readonly', True)],
                                          'inspect': [('readonly', True)],
                                        })
    fault_method_id = fields.Many2one("maintain.fault.method", ondelete='set null',
                                      string="Fault Method", states={
                                          'completed': [('readonly', True)],
                                          'inspect': [('readonly', True)],
                                        })
    fault_method_code = fields.Char(related='fault_method_id.fault_method_code', store=True, readonly=True)

    work_time = fields.Float(compute='_get_work_time', store=True, readonly=True, copy=True, string="Work Time(Hours)")
    warranty_deadline = fields.Integer(related='fault_method_id.warranty_deadline', string="Warranty Deadline(Days)",
                                       readonly=1, required=True) #保修天数 与返修逻辑有关
    plan_start_time = fields.Datetime("Plan Start Time", help="Plan Start Time")
    plan_end_time = fields.Datetime("Plan End Time", help="Plan End Time", compute='_get_end_datetime')
    real_start_time = fields.Datetime("Real Start Time", help="Real Start Time")
    real_end_time = fields.Datetime("Real End Time", help="Real End Time")
    user_id = fields.Many2one('hr.employee', string="Repair Name")

    repair_names = fields.Char(string='Repair Names', help="Repair Names", compute='_get_repair_names')
    state = fields.Selection([
        ('draft', "Draft"),
        ('wait_dispatch', "Wait Dispatch"),
        ('wait_repair', "Wait Repair"),
        ('repair', "Repair"),
        ('inspect', "Inspect"),
        ('completed', "Completed")], default='draft', string="Repair State", copy=True)

    repair_type = fields.Selection([('vehicle_repair', "vehicle_repair"),
                                    ('assembly_repair', "assembly_repair")],
                                   default='vehicle_repair', string="Repair Type")

    job_ids = fields.One2many("maintain.manage.repair_jobs", 'repair_id', string='Maintain Repair Jobs',
                              states={
                                  'completed': [('readonly', True)],
                                  'inspect': [('readonly', True)],
                                  'repair': [('readonly', True)],
                              }, copy=True)
    percentage_work = fields.Float(help='percentage_work', digits=(5, 1), default=100.0)

    materials_control = fields.Boolean("Materials Control", readonly=True)
    available_product_ids = fields.One2many("maintain.manage.available_product", 'repair_id',
                                            string='Available Product', copy=True)
    operation_manual = fields.Text("Operation Manual", related='fault_method_id.operation_manual',
                                   help="Operation Manual", store=True, readonly=True)
    inspect_standard = fields.Text("Inspect Standard", related='fault_method_id.inspect_standard',
                                   help="Inspect Standard", store=True, readonly=True)

    picking_ids = fields.One2many("stock.picking", 'repair_id', string='Stock Pickings', copy=False) #物料单

    return_repair_state = fields.Selection([('yes', "yes"), ('no', "no"), ('doubt', "doubt")],
                                           default='no', string="Return Repair State",states={
                                          'completed': [('readonly', True)],
                                          'inspect': [('readonly', True)],
                                        }) #返修状态

    return_repair_type = fields.Selection(
                            [('vehicle quality problems(manufacturer)', "vehicle quality problems(manufacturer)"),
                             ('material problem(suppliers)', "material problem(suppliers)"),
                             ('repair(repair)', "repair(repair)"),
                             ('traffic problems(lines)', 'traffic problems(lines)'),
                             ('driving problem(driver)', 'driving problem(driver)')],
                            states={
                                'completed': [('readonly', True)],
                                'inspect': [('readonly', True)],
                            }
                        )#返修类型

    return_repair_ids = fields.Many2many('maintain.manage.repair', 'maintain_manage_repair_return_rel', 'return_repair_id',
                                         'repair_id', string='Return Repair Order', states={
                                                        'completed': [('readonly', True)],
                                                        'inspect': [('readonly', True)],
                                                        # 'repair': [('readonly', True)],
                                                        }
                                         )#返修对象

    return_repair_names = fields.Char("Return Repair Names") #返修人

    #2017年7月25日 新增字段：抢修总时长
    repair_total_time = fields.Float(string='Repair total time', readonly=True,
                                    digits=dp.get_precision('Operate pram'), compute='_compute_repair_total_time')
    repair_start_time = fields.Datetime(related='report_id.preflight_date', string='Repair start time')

    is_change = fields.Boolean("Is change", default=False) #更改维修方法后变成True 开工后变成False 判断第一次派工和修改维修方法派工的只读
    is_method_change = fields.Boolean("is_method_change", default=False) #更改维修方法后变成 变化的单据，退料时有用
    active = fields.Boolean("Active", default=True)

    change_method_ids = fields.One2many("maintain.manage.repair_change_method", 'repair_id',
                                        string='repair_change_method') #维修方法的修改轨迹

    origin_repair_id = fields.Many2one('maintain.manage.repair',
                                ondelete='cascade', string="Origin Repair")

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {},
                       name=_('%s_copy_%s') % (self.name, time.strftime("%Y%m%d%H%M%S")),
                       origin_repair_id=self.id
                       )
        return super(MaintainRepair, self).copy(default)

    @api.depends('fault_method_id', 'vehicle_type')
    def _get_work_time(self):
        #维修单 额定工时计算：根据车型，维修方法计算指定 额定类型的时长
        for order in self:
            time_type = order.vehicle_type.time_type_id
            work_time_line = order.fault_method_id.work_time_lines.filtered(lambda x: x.time_type_id == time_type)
            order.work_time = work_time_line.work_time

    @api.depends('repair_start_time', 'end_inspect_time')
    def _compute_repair_total_time(self):
        """
            计算抢修总时长
        :return:
        """
        for order in self:
            if order.repair_start_time and order.end_inspect_time:
                repair_start_time = datetime.datetime.strptime(order.repair_start_time, "%Y-%m-%d %H:%M:%S")
                end_inspect_time = datetime.datetime.strptime(order.end_inspect_time, "%Y-%m-%d %H:%M:%S")
                order.repair_total_time = (end_inspect_time - repair_start_time).seconds/3600.0

    @api.onchange('return_repair_ids')
    def _get_return_repair_names(self):
        """
        获取返修单中的返修人员
        :return:
        """
        for i in self:
            repair_names_list=[]
            for j in i.return_repair_ids:
                repair_names_list.append(j.repair_names)
            i.return_repair_names = ':'.join(list(set(repair_names_list)))

    @api.multi
    def unlink(self):
        """
        控制单据的删除，只能删除草稿状态的单据
        :return:
        """
        for order in self:
            if not order.state == 'draft':
                raise exceptions.UserError(_('In order to delete a repair order, you must set it draft first.'))

        return super(MaintainRepair, self).unlink()

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
            r.plan_end_time = start + timedelta(seconds=r.work_time*3600)

    @api.multi
    def write(self, vals):
        is_change = False
        is_method_change = False
        if 'return_repair_state' in vals:
            return_repair_state = vals.get('return_repair_state')
            if return_repair_state == 'doubt':
                raise exceptions.UserError(_('Maintenance exists the type is doubt, please set to yes or no'))
            elif return_repair_state == 'yes':
                if self.name.startswith("WXD"):
                    vals.update({'name': self.name.replace('WXD', 'FXD')})

        if "fault_method_id" in vals and vals.get('fault_method_id'):
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
                        'list_price':j.list_price,
                    }
                    datas.append((0, 0, data))
            vals.update({'available_product_ids': datas,
                         'materials_control':method.materials_control,
                        })
            if self.env.context['is_change_method']: #如果时更改维修方法
                old_rec = self.copy({'active': False, 'state': self.env.context['state']})
                old_rec.job_ids.write({"real_end_time": fields.Datetime.now()})
                data_methods = []
                data_method = {
                    "old_category_id": old_rec.fault_category_id.id,
                    "old_appearance_id":old_rec.fault_appearance_id.id or None,
                    "old_reason_id": old_rec.fault_reason_id.id,
                    "old_method_id":  old_rec.fault_method_id.id,

                    "new_category_id": vals.get('fault_category_id') or old_rec.fault_category_id.id,
                    "new_appearance_id": vals.get('fault_appearance_id') or old_rec.fault_appearance_id.id or None,
                    "new_reason_id": vals.get('fault_reason_id') or old_rec.fault_reason_id.id,
                    "new_method_id": vals.get('fault_method_id'),
                    "user_id":self._default_employee().id if self._default_employee() else ''
                }
                data_methods.append((0, 0, data_method))
                is_change = True
                is_method_change = True
                vals.update({'is_change':is_change,
                             'is_method_change':is_method_change,
                             'job_ids': [(5, 0, 0)],
                             'change_method_ids':data_methods,
                             })
            self.available_product_ids.unlink()  # 维修单存在物料清单，要删除
        res = super(MaintainRepair, self).write(vals)
        return res

    @api.onchange('percentage_work')
    def _verify_percentage_work(self):
        """
        维修单:
           功能：验证百分比的大小 不能小于0或者大于100
        """
        if self.percentage_work < 0 or self.percentage_work > 100:
            return {
                'warning': {
                    'title': u"不正确的值",
                    'message': u"工时比例数必须大于0和小于100",
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

            work_time_line = self.fault_method_id.work_time_lines.filtered(lambda x: x.time_type_id == self.vehicle_type.time_type_id)
            self.work_time = work_time_line.work_time

            if self.fault_method_id.reason_id.appearance_id:
                self.fault_appearance_id = self.fault_method_id.reason_id.appearance_id
                self.fault_category_id = self.fault_method_id.reason_id.appearance_id.category_id
            else:
                self.fault_category_id = self.fault_method_id.reason_id.category_id
                self.fault_appearance_id = None

            domain = [('vehicle_id', '=', self.vehicle_id.id),
                         ('state', '=', 'completed'),
                         ('fault_method_id', '=', self.fault_method_id.id),
                         ('end_inspect_time', '>=', fields.Datetime.to_string(fields.datetime.now() - timedelta(days=self.warranty_deadline)))
                         ]

            res = self.search(domain)
            if res:
                self.return_repair_state = 'doubt'
                self.return_repair_ids = [(6, 0, res.ids)]
            else:
                self.return_repair_state = 'no'
                self.return_repair_ids = []

    @api.model
    def create(self, vals):
        """
        维修单:
            自动生成订单号：前缀WXD+序号
        """
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('maintain.manage.repair') or '/'
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
        if self.job_ids:
            method_list = self.job_ids.mapped('fault_method_id')
            if len(method_list) !=1 or self.fault_method_id.id != method_list[0].id:
                raise exceptions.UserError(u'工时管理的维修方法必须一致')

        #派工时再判断工时比例
        if self.percentage_work <=0 or self.percentage_work > 100:
            raise exceptions.UserError(u'工时比例数必须大于0和小于100')
        percentage_work = sum(i.percentage_work for i in self.job_ids)
        if percentage_work + self.percentage_work > 100:
            raise exceptions.UserError(_("Dispatching the proportion of more than 100"))
        # self.state = 'wait_repair'
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
            'percentage_work': 100 - percentage_work - self.percentage_work,
            "user_id": False,
            # 'plan_start_time': False,
            # 'state': 'wait_repair',
            'job_ids': [(0, 0, vals)]
        })

        form_view_ref = self.env.ref('vehicle_maintain.maintain_repair_view_form_action', False)

        return {
            'name': _('action_dispatch'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'maintain.manage.repair',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_id': False,
            'views': [(form_view_ref and form_view_ref.id, 'form')],
        }

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
        self.write({'state': 'repair',
                    'is_change':False})

        for i in self.job_ids:
            i.real_start_time = fields.Datetime.now()
        if self.materials_control:
            avail_products = self.mapped('available_product_ids').filtered(lambda x: x.change_count > 0)
            location_dest_id = self.env.ref('stock_picking_types.stock_location_ullage').id  # 维修(生产)虚位
            self._generate_picking(avail_products, location_dest_id)

    def _generate_picking(self, products, location):
            picking_type = self.env['stock.picking.type'].search([('name','=',u'发料'),('warehouse_id.company_id','=',self.env.user.company_id.id)])
            #picking_type = self.env.ref('stock_picking_types.picking_type_issuance_of_material')
            # location_id = self.env.ref('stock.stock_location_stock').id     # 库存

            location_id = picking_type.default_location_src_id.id or picking_type.warehouse_id.lot_stock_id.id

            for products in [products]:
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
                        'picking_type_id': picking_type.id,
                    }
                    move_lines.append((0, 0, vals))
                if move_lines:
                    picking = self.env['stock.picking'].create({
                        'origin': self.name,
                        'location_id': location_id,
                        'location_dest_id': location,
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
        picking_type = self.env['stock.picking.type'].search(
            [('name', '=', u'领料'), ('warehouse_id.company_id', '=', self.env.user.company_id.id)])
        context = dict(self.env.context,
                       default_repair_id=self.id,
                       default_origin=self.name,
                       default_picking_type_id=picking_type.id,
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
        picking_type = self.env['stock.picking.type'].search(
            [('name', '=', u'退料'), ('warehouse_id.company_id', '=', self.env.user.company_id.id)])
        context = dict(self.env.context,
                       default_repair_id=self.id,
                       default_origin=self.name,
                       default_picking_type_id=picking_type.id,
                       # default_picking_type_id=self.env.ref('stock_picking_types.picking_type_return_material').id,
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
    def comfirm_dispatch(self):
        self.ensure_one()
        is_change_method = self.env.context.get('is_change_method')
        if is_change_method:
            if self.is_change:
                self.write({'state':'wait_dispatch'})

                context = dict(self.env.context,
                               default_is_change_method=is_change_method,
                               )
                context['state'] = self.state
                context['is_change_method'] = 0
                context['is_change_method_readonly'] = 1

                form_view_ref = self.env.ref('vehicle_maintain.maintain_repair_view_form_action', False)
                return {
                    'name': _('Change Method'),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'maintain.manage.repair',
                    'res_id': self.id,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'view_id': False,
                    'views': [(form_view_ref and form_view_ref.id, 'form')],
                    'context': context
                }
            else:
                return False

        if not self.job_ids:
            raise exceptions.UserError(_("Maintain Repair Jobs Required!"))
        self.write({'state':'wait_repair'})
        return True

    @api.multi
    def action_dispatch(self):
        self.ensure_one()
        is_change_method = self.env.context.get('is_change_method')

        context = dict(self.env.context,
                       default_is_change_method=is_change_method,
                       )
        context['is_change_method_readonly'] = 0
        if self.is_change:
            context['is_change_method_readonly'] = 1
        context['state'] = self.state
        form_view_ref = self.env.ref('vehicle_maintain.maintain_repair_view_form_action', False)

        return {
            'name': _('action_dispatch'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'maintain.manage.repair',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_id': False,
            'views': [(form_view_ref and form_view_ref.id, 'form')],
            'context': context
        }


class MaintainRepairChangeMethod(models.Model):

    _name = 'maintain.manage.repair_change_method'
    _order = "id desc"

    repair_id = fields.Many2one('maintain.manage.repair',
                                ondelete='cascade', string="Repair")

    old_category_id = fields.Many2one("maintain.fault.category", ondelete='set null',
                                        string="Old Category")
    old_appearance_id = fields.Many2one("maintain.fault.appearance", ondelete='set null',
                                          string="Old Appearance")
    old_reason_id = fields.Many2one("maintain.fault.reason", ondelete='set null', string="Old Reason")
    old_method_id = fields.Many2one("maintain.fault.method", ondelete='set null', string="Old Method")

    new_category_id = fields.Many2one("maintain.fault.category", ondelete='set null',
                                        string="New Category")
    new_appearance_id = fields.Many2one("maintain.fault.appearance", ondelete='set null',
                                          string="New Appearance")
    new_reason_id = fields.Many2one("maintain.fault.reason", ondelete='set null', string="New Reason")
    new_method_id = fields.Many2one("maintain.fault.method", ondelete='set null', string="New Method")

    user_id = fields.Many2one('hr.employee', string="Change Name", required=True)


class MaintainAvailableProduct(models.Model):
    _name = 'maintain.manage.available_product'

    repair_id = fields.Many2one('maintain.manage.repair',
                                ondelete='cascade', string="Repair")
    method_id = fields.Many2one('maintain.fault.method',
                                ondelete='set null', string="Fault Method Name")

    product_id = fields.Many2one('product.product', string="Product Name")
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
    list_price = fields.Float("Stock Price")
    change_count = fields.Integer("Change Count")
    max_count = fields.Integer("Max Count")


class MaintainRepairJobs(models.Model):
    """
    车辆维修管理：维修单工时管理
    """
    _name = 'maintain.manage.repair_jobs'
    name = fields.Char("Job Name", help="Job Name")
    sequence = fields.Integer("Sequence", help="Sequence")
    repair_id = fields.Many2one("maintain.manage.repair", ondelete='cascade',
                                string="Maintain Repair")
    fault_category_id = fields.Many2one("maintain.fault.category", ondelete='set null',
                                        string="Fault Category")
    fault_appearance_id = fields.Many2one("maintain.fault.appearance", ondelete='set null',
                                          string="Fault Appearance")
    fault_reason_id = fields.Many2one("maintain.fault.reason", ondelete='set null', string="Fault Reason")
    fault_method_id = fields.Many2one("maintain.fault.method", ondelete='set null', string="Fault Method")
    user_id = fields.Many2one('hr.employee', string="Repair Name", required=True)
    plan_start_time = fields.Datetime("Plan Start Time")
    plan_end_time = fields.Datetime("Plan End Time")
    real_start_time = fields.Datetime("Real Start Time")
    real_end_time = fields.Datetime("Real End Time")
    percentage_work = fields.Float('Percentage Work')
    work_time = fields.Float('Work Time(Hour)', digits=(10, 2))
    my_work = fields.Float('My Work(Hour)', digits=(10, 2), compute='_get_my_work', store=True)

    real_work = fields.Float('Real Work(Hour)', digits=(10, 2), compute="_get_real_work", store=True)

    @api.depends('real_start_time', 'real_end_time')
    def _get_real_work(self):
        for i in self:
            if i.real_start_time and i.real_end_time:
                start_time = fields.Datetime.from_string(i.real_start_time)
                end_time = fields.Datetime.from_string(i.real_end_time)
                i.real_work = (end_time-start_time).seconds/3600.0

    @api.depends('work_time', 'percentage_work')
    def _get_my_work(self):
        for i in self:
            i.my_work = i.work_time * i.percentage_work/100


class MaintainInspect(models.Model):
    """
    车辆维修管理：检验单
    """
    # _name = 'maintain.maintain_inspect'
    _inherit = 'maintain.manage.repair'

    inspect_result = fields.Selection([('qualified', 'Qualified'),
                                       ('defective','Defective')], string="Inspect Result")

    start_inspect_time = fields.Datetime("Start Inspect Time")
    end_inspect_time = fields.Datetime("End Inspect Time")
    return_record_ids = fields.One2many("maintain.manage.return_record", 'repair_id', string='Maintain Repair')

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False
    inspect_user_id = fields.Many2one('hr.employee', string="Inspect Name")
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
            i.inspect_user_id = self._default_employee()

            if all(repair.state in ['completed'] for repair in i.report_id.repair_ids):
                i.report_id.state = 'completed'
                i.report_id.vehicle_id.state = 'normal' #所有的抢修单据完成后更新车辆状态
            i._refresh_jobs() #更新所有工时管理

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
        inspect_user_id = self._default_employee().id if self._default_employee() else ''
        vals = {
            "repair_id": self.id,
            "inspect_return_time": inspect_return_time,
            "return_reason": reason,
            "inspect_user_id":inspect_user_id,
            "sequence": len(self.return_record_ids) + 1
        }
        self.write({
            "state":'repair',
            "end_inspect_time": inspect_return_time,
            "inspect_result": "defective",
            "inspect_user_id": inspect_user_id,
            "return_record_ids": [(0, 0, vals)]
        })


class MaintainReturnRecord(models.Model):
    """
    退检记录
    """
    _name = 'maintain.manage.return_record'
    repair_id = fields.Many2one('maintain.manage.repair', string="Repair Order",
                                required=True, readonly=True)
    inspect_user_id = fields.Many2one('hr.employee',  string="Inspect Name",
                                      readonly=True)
    repair_names = fields.Char(string='Repair Names',related='repair_id.repair_names')
    fault_method_id = fields.Many2one("maintain.fault.method", related='repair_id.fault_method_id',
                                      ondelete='set null', string="Fault Method")
    return_reason = fields.Text("Return Reason")
    inspect_return_time = fields.Datetime("Inspect Return Time")
    sequence = fields.Integer("Sequence")
