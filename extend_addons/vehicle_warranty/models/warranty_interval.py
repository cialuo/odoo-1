# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class WarrantyInterval(models.Model): # 维保间隔
    _name = 'warranty_interval'
    _order = 'vehicle_model_id,interval_mileage'

    name = fields.Char(default="")

    sequence = fields.Integer('Cycle Sequence', default=1)

    warranty_category_id = fields.Many2one('warranty_category', 'Warranty Category', domain=[('level', '=', '1')], ondelete='set null', required=True)  # 保养类别

    interval_mileage = fields.Float(digits=(6, 1), string="Interval Mileage", default=10000)  # 间隔里程

    state = fields.Selection([ # 状态
        ('use', "use"), # 在用
        ('done', "Filing"),  # 归档
    ], default='use',string="MyState")

    active = fields.Boolean(string="MyActive", default=True)

    vehicle_model_id = fields.Many2one("fleet.vehicle.model", ondelete='set null', required=True)  # 车型

    @api.multi
    def action_in_use(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_filing(self):
        self.state = 'done'
        self.active = False

    @api.constrains('interval_mileage')
    def _check_interval_mileage(self):
        for r in self:
            if r.interval_mileage <= 0:
                raise exceptions.ValidationError(_("interval_mileage must be greater than or equal to zero"))

    _sql_constraints = [
        ('category_interval_mileage_unique', 'unique(vehicle_model_id, warranty_category_id, interval_mileage)', _('The category and mileage must be unique!'))
    ]


class FleetVehicleModel(models.Model): # 车型管理
    _inherit = 'fleet.vehicle.model'
    warranty_interval_ids = fields.One2many('warranty_interval', 'vehicle_model_id', string="Warranty Interval Ids")


class WarrantyCapability(models.Model): # 保养能力参数设置
    _name = 'warranty_capability'

    name = fields.Char(default="")

    sequence = fields.Integer('Sequence', default=0, readonly="true")

    warranty_category_id = fields.Many2one('warranty_category', 'Warranty Category', domain=[('level', '=', '1')], ondelete='set null', required=True)  # 保养类别

    company_id = fields.Many2one('hr.department', string='United', required=True)

    warranty_vehicle_count = fields.Integer('Warranty Vehicle Count', default=1)

    remark = fields.Text("Remark", help="Remark")

    @api.model
    def create(self, vals):
        if vals.get('sequence', 0) == 0:
            vals['sequence'] = self.env['ir.sequence'].next_by_code('warranty.capability') or 0
        return super(WarrantyCapability, self).create(vals)

    @api.constrains('warranty_vehicle_count')
    def check_warranty_vehicle_count(self):
        """
            校验：保养车辆数
        :return:
        """
        for order in self:
            if order.warranty_vehicle_count <= 0:
                raise exceptions.ValidationError(_("warranty_vehicle_count Can not be negative！"))

class WarrantyLevel(models.Model):  # 维保级别
    _name = 'warranty_level'

    name = fields.Char(required=True)

    _sql_constraints = [('warranty_level_name_unique', 'unique(name)', 'Level name already exists')]


