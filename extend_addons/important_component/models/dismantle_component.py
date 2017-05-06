# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields
import odoo.addons.decimal_precision as dp

class DismantleComponent(models.Model):
    _name = 'dismantle.component'

    """
    要件变更记录
    """
    component_id = fields.Many2one('product.component', string='Component')
    component_code = fields.Char(string='Component Code', related='component_id.code', store=True)
    product_id = fields.Many2one('product.product', related='component_id.product_id', string='Component Type', store=True)
    install_date = fields.Date(string='Install Date')
    install_type = fields.Selection([('within_vehicle', 'Within Vehicle'), ('repair', 'Repair')], string='Install type')
    dismantle_type = fields.Selection([('fault', 'Fault'), ('other', 'Other')], string='Dismantle type')
    install_user = fields.Many2one('res.users', string='Install User')
    dismantle_user = fields.Many2one('res.users', string='Dismantle User')
    dismantle_date = fields.Date(string='Dismantle Date')
    operate_days = fields.Float(string='Operating Days', digits=dp.get_precision('Operate pram'))
    operate_mileage = fields.Float(string='Operating Mileage', digits=dp.get_precision('Operate pram'))
    vehicle_id =fields.Many2one('fleet.vehicle', string='Vehicle')

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    dismantle_ids = fields.One2many('dismantle.component', 'vehicle_id', string='Dismantle')