# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class WarrantyInterval(models.Model): # 维保间隔
    _name = 'warranty_interval'

    name = fields.Char()

    sequence = fields.Integer('Cycle Sequence', default=1, readonly="true")

    warranty_category_id = fields.Many2one('warranty_category', 'Warranty Category', domain=[('level', '=', '1')], ondelete='set null', required=True)  # 保养类别

    interval_mileage = fields.Float(digits=(6, 1), string="Interval Mileage", default=10000)  # 间隔里程

    state = fields.Selection([ # 状态
        ('in_use', "in_use"), # 在用
        ('filing', "filing"),  # 归档
    ], default='in_use',string="MyState")

    vehicle_model_id = fields.Many2one("fleet.vehicle.model", ondelete='set null', required=True)  # 车型

    @api.multi
    def action_in_use(self):
        self.state = 'in_use'

    @api.multi
    def action_filing(self):
        self.state = 'filing'

    @api.constrains('interval_mileage')
    def _check_interval_mileage(self):
        for r in self:
            if r.interval_mileage <= 0:
                raise exceptions.ValidationError(_("interval_mileage must be greater than or equal to zero"))



class WarrantyCapability(models.Model): # 保养能力参数设置
    _name = 'warranty_capability'

    name = fields.Char()

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


class WarrantyLevel(models.Model):  # 维保级别
    _name = 'warranty_level'

    name = fields.Char(required=True)

    _sql_constraints = [('warranty_level_name_unique', 'unique(name)', 'Level name already exists')]


