# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class VehiclePlant(models.Model):
    """
    维修厂
    """
    _name = "vehicle.plant"
    _sql_constraints = [('name_uniq', 'unique (name)', _("plant name already exists")),
                        ('plant_code_uniq', 'unique(plant_code)', _('The plant code must be unique')),]

    name = fields.Char("Plant Name", required=True)
    plant_code = fields.Char(string="Plant Code", required=True)
    department_id = fields.Many2one('hr.department', required=True, domain="[('departmenttype', '=', 'maintainfactory')]")
    company_id = fields.Many2one('res.company', related='department_id.company_id', store=True)
    scale = fields.Char("Plant Scale")
    active = fields.Boolean(default=True)
    address =  fields.Char("Plant Address")
    state = fields.Selection([('use', "Use"), ('done', "Done")], default='use')

    # employee_ids = fields.One2many('vehicle.plant.employee', 'plant_id', string="Plant Employee")
    employee_ids = fields.One2many('hr.employee', 'department_id',
                                   compute='_compute_employee_ids',string="Plant Employee")

    # employee_ids = fields.One2many('hr.employee', 'department_id',
    #                                string='department employees',
    #                                domain="[('workpost.posttype', '=', maintainer)]",
    #                                related='department_id.member_id')

    ditch_ids = fields.One2many('vehicle.plant.ditch','plant_id',string='Ditch ids')

    @api.depends('department_id')
    def _compute_employee_ids(self):
        for i in self:
            members = i.department_id.member_id.filtered(lambda x: x.workpost.posttype == 'maintainer')
            i.employee_ids = members



    # @api.onchange('department_id')
    # def onchange_department_id(self):
    #     if self.department_id:
    #         members = self.department_id.member_id
    #         data = []
    #         for i in members.filtered(lambda x: x.workpost.posttype == 'maintainer'):
    #             vals = {
    #                 'plant_id': self.id,
    #                 "plant_employee_id": i.id,
    #             }
    #
    #             data.append((0, 0, vals))
    #         self.employee_ids = data


    @api.multi
    def action_use(self):
        self.state = 'use'
        self.active = True

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.active = False

class VehiclePlantDitch(models.Model):

    _name ='vehicle.plant.ditch'
    _description = 'Vehicle plant ditch'

    name = fields.Char('Ditch Name',required=True)

    plant_id = fields.Many2one('vehicle.plant',string='Plant Id')

    ditch_type = fields.Selection([('vehicleWarranty','vehicleWarranty'),('vehicleMaintain','vehicleMaintain')],string='Ditch type')

    remarks = fields.Char(string='remarks')

    work_time = fields.Selection([('Monday','Monday'),
                                  ('Tuesday','Tuesday'),
                                  ('Wednesday','Wednesday'),
                                  ('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday'),('Sunday','Sunday')],string='Ditch Work time')




# class PlantEmployee(models.Model):
#     """
#     维修工列表
#     """
#     _name='vehicle.plant.employee'
#
#     plant_id = fields.Many2one("vehicle.plant")
#
#     plant_employee_id = fields.Many2one("hr.employee")
#
#     jobnumber = fields.Char(string='employee work number', related='plant_employee_id.jobnumber')
#     title = fields.Char(string='employee title', related='plant_employee_id.title')
#     workpost = fields.Many2one('employees.post', related='plant_employee_id.workpost', string='employee work post')
#
#     mobile_phone = fields.Char(related='plant_employee_id.mobile_phone')