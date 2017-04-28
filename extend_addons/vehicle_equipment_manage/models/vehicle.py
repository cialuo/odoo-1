# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Vehicle(models.Model):
    """
    车辆档案
    """
    _inherit = "fleet.vehicle"

    equipment_ids = fields.One2many('vehicle_equipment.equipment', "vehicle_id", string="Vehicle Equipment")


class VehicleEquipment(models.Model):
    """
    随车设备
    """
    _name = 'vehicle_equipment.equipment'

    vehicle_id = fields.Many2one('fleet.vehicle', ondelete='set null', string="Vehicle")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment", required=True)
    serial_no = fields.Char("Serial No", related='equipment_id.serial_no')
    fixed_asset_number = fields.Char("Fixed Asset Number", help="Fixed Asset Number")
    create_date_ext = fields.Datetime("Create Date", related='equipment_id.create_date')