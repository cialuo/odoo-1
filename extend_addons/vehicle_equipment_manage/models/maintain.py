# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import timedelta


class MaintainReport(models.Model):
    """
    车辆维修管理：报修单
    """
    _inherit = 'maintain.manage.report'

    def _default_employee(self):
        emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        return emp_ids and emp_ids[0] or False

    @api.multi
    def action_precheck_to_repair(self):
        """
        预检单:
            功能：预检通过并创建交接单
            状态：预检->维修
        """
        res = super(MaintainReport, self).action_precheck_to_repair()
        self.ensure_one()

        def _default_employee(self):
            emp_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
            return emp_ids and emp_ids[0] or False

        report_user_id = self._default_employee()
        equipment_lines = []
        for i in self.vehicle_id.equipment_ids:
            vals = {
                'equipment_id': i.equipment_id.id,
                'serial_no': i.serial_no,
                'fixed_asset_number': i.fixed_asset_number,
                'create_date_ext': i.create_date_ext,
            }
            equipment_lines.append([0, 0, vals])

        data = {
            "report_id": self.id,
            "report_user_id": report_user_id.id,
            'equipment_ids': equipment_lines
        }

        deliverys = self.env['vehicle_equipment.maintain.delivery'].search([("report_id", '=', self.id)])
        if not deliverys:
            self.env['vehicle_equipment.maintain.delivery'].create(data)
        return res

    @api.multi
    def delivery_manage(self):
        """
        预检单:
            功能：跳转到交接单
        """
        self.ensure_one()
        deliverys = self.env['vehicle_equipment.maintain.delivery'].search([("report_id", '=', self.id)])
        action = self.env.ref('vehicle_equipment_manage.maintain_delivery_action').read()[0]
        action['res_id'] = deliverys.id
        action['views'] = [(self.env.ref('vehicle_equipment_manage.maintain_delivery_view_form').id, 'form')]
        return action


class MaintainDelivery(models.Model):
    """
    车辆维修管理：交接单
    """
    _inherit = 'mail.thread'
    _name = 'vehicle_equipment.maintain.delivery'

    name = fields.Char(string="Delivery Order", help='Delivery Order', required=True, index=True,
                       copy=False, default='/')
    report_id = fields.Many2one("maintain.manage.report", ondelete='cascade', string="Report Order")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No',
                                 related='report_id.vehicle_id', store=True, readonly=True, copy=False)
    vehicle_type = fields.Many2one("fleet.vehicle.model", related='report_id.vehicle_id.model_id',
                                   store=True, readonly=True, copy=False)
    license_plate = fields.Char(string="License Plate",
                                related='report_id.vehicle_id.license_plate', store=True, readonly=True, copy=False)

    report_user_id = fields.Many2one('hr.employee', string="Create Name", required=True, readonly=True)

    delivery_time = fields.Datetime("Delivery Time", readonly=True)
    delivery_return_time = fields.Datetime("Delivery Return Time", readonly=True)

    state = fields.Selection([
        ('draft', "Draft"),
        ('delivery', "Delivery"),
        ('return', "Return")], default='draft')

    equipment_ids = fields.One2many('vehicle_equipment.maintain.equipment', 'delivery_id', string='Deliverys')
    equipment_return_ids = fields.One2many('vehicle_equipment.maintain.return_equipment', 'delivery_id',
                                           string='Return Deliverys')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('vehicle_equipment.maintain.delivery') or '/'
        return super(MaintainDelivery, self).create(vals)

    @api.multi
    def action_delivery(self):
        self.state = 'delivery'
        self.delivery_time = fields.Datetime.now()

    @api.multi
    def action_return(self):
        self.state = 'return'
        self.delivery_return_time = fields.Datetime.now()
        equipment_lines = []
        for i in self.equipment_ids:
            vals = {
                'equipment_id': i.equipment_id.id,
                'serial_no': i.serial_no,
                'fixed_asset_number': i.fixed_asset_number,
                'create_date_ext': i.create_date_ext,
            }
            equipment_lines.append([0, 0, vals])
        self.equipment_return_ids = equipment_lines

    @api.multi
    def action_delivery_to_repair(self):
        """
        交接单:
            功能：交接单跳转到维修单
        """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('vehicle_maintain', xml_id)
            res.update(
                context=dict(self.env.context, default_report_id=self.report_id.id),
                domain=[('report_id', '=', self.report_id.id)]
            )
            print res
            return res
        return False


class VehicleEquipmentMaintain(models.Model):
    """
    交接清单
    """
    _name = 'vehicle_equipment.maintain.equipment'

    delivery_id = fields.Many2one('vehicle_equipment.maintain.delivery', ondelete='cascade', string="Delivery")

    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")
    serial_no = fields.Char("Serial No")
    name = fields.Char("Name")
    fixed_asset_number = fields.Char("Fixed Asset Number")
    create_date_ext = fields.Datetime("Create Date")


class VehicleEquipmentMaintainReturn(models.Model):
    """
    交回清单
    """
    _name = 'vehicle_equipment.maintain.return_equipment'

    delivery_id = fields.Many2one('vehicle_equipment.maintain.delivery', ondelete='cascade', string="Delivery")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")
    serial_no = fields.Char("Serial No")
    name = fields.Char("Name")
    fixed_asset_number = fields.Char("Fixed Asset Number")
    create_date_ext = fields.Datetime("Create Date")


