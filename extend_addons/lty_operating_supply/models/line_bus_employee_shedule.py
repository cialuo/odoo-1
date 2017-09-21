# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.sql import drop_view_if_exists

class line_bus_employee_shedule(models.Model):
    _name = 'line.bus.employee.shedule'
    _auto = False
    _order = 'bus_code asc'
    
    id = fields.Char()
    company_id = fields.Many2one('res.company')
    line_id = fields.Many2one('route_manage.route_manage')
    bus_model = fields.Many2one('fleet.vehicle.model')
    bus_model_name = fields.Char()
    bus_code = fields.Char()
    entry_state = fields.Char()
    workpost_id = fields.Many2one('employees.post')
    jobnumber = fields.Char()
    employee_name = fields.Char()
    workpost_name = fields.Char()

    @api.model_cr
    def init(self):
        drop_view_if_exists(self._cr, 'line_bus_employee_shedule')
        self._cr.execute("""
            CREATE OR REPLACE VIEW line_bus_employee_shedule AS (
				select
                   hr_employee_route_manage_route_manage_rel.hr_employee_id ::text||hr_employee_route_manage_route_manage_rel.route_manage_route_manage_id::text ||fleet_vehicle.id::text as id ,
				   fleet_vehicle.company_id,
				   fleet_vehicle.route_id as line_id,
				   fleet_vehicle.model_id as bus_model,
				   fleet_vehicle_model.name as bus_model_name,
				   fleet_vehicle.vehicle_code as bus_code,
				   fleet_vehicle.entry_state,
				   hr_employee.workpost as workpsot_id,
				   hr_employee.jobnumber,
				   hr_employee.name_related as employee_name,
				   employees_post.name as workpost_name
				from 
					hr_employee_route_manage_route_manage_rel 
				left join hr_employee on hr_employee_route_manage_route_manage_rel.hr_employee_id = hr_employee.id
				left join fleet_vehicle on hr_employee_route_manage_route_manage_rel.route_manage_route_manage_id = fleet_vehicle.route_id
				left join fleet_vehicle_model on fleet_vehicle_model.id = fleet_vehicle.model_id
				left join employees_post on employees_post.id = hr_employee.workpost
				where 
					fleet_vehicle.route_id is not null order by fleet_vehicle.vehicle_code				
            )""")        
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
