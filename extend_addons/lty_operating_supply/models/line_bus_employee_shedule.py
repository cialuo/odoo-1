# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.sql import drop_view_if_exists

class line_bus_employee_shedule(models.Model):
    _name = 'line.bus.employee.shedule'
    _auto = False
    _order = 'bus_code asc'
    
    id = fields.Char()
    company_id = fields.Many2one('hr.department')
    bus_group_id = fields.Many2one('bus_group')
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
                    bus_code::text||jobnumber::text||bus_group_id::text as id,
                    company_id,bus_group_id,line_id,bus_model,bus_model_name,bus_code,workpsot_id,jobnumber,employee_name,workpost_name,
                    (case entry_state
                         when 'draft' then '草稿'
                         when 'submitted' then '已提交'
                         when 'audited' then '已审核'
                          end) entry_state
                    from (
                     (select
                         fleet_vehicle.company_id, 
                         bus_group.route_id as line_id,
                         bus_group.id as bus_group_id,
                         fleet_vehicle.model_id as bus_model,
                         fleet_vehicle_model.name as bus_model_name,
                         fleet_vehicle.vehicle_code as bus_code,
                         fleet_vehicle.entry_state,
                         hr_employee.workpost as workpsot_id,
                         hr_employee.jobnumber,
                         employees_post.name as workpost_name,
                         hr_employee.name_related as employee_name   
                     from 
                         bus_group_driver_vehicle_shift
                     left join 
                         bus_group on bus_group.id = bus_group_driver_vehicle_shift.group_id
                     left join
                         bus_group_vehicle on bus_group_vehicle.id = bus_group_driver_vehicle_shift.bus_group_vehicle_id    
                     left join
                         fleet_vehicle on bus_group_vehicle.vehicle_id = fleet_vehicle.id
                     left join fleet_vehicle_model on fleet_vehicle_model.id = fleet_vehicle.model_id
                     left join 
                         bus_group_conductor on bus_group_conductor.id = bus_group_driver_vehicle_shift.conductor_id
                     left join 
                         hr_employee on bus_group_conductor.conductor_id = hr_employee.id
                     left join employees_post on employees_post.id = hr_employee.workpost
                     where   
                        bus_group_driver_vehicle_shift.conductor_id is not null and bus_group_driver_vehicle_shift.active = true
                     group by 
                         bus_group_driver_vehicle_shift.conductor_id,
                         bus_group.route_id,
                         hr_employee.workpost,
                         hr_employee.jobnumber,
                         hr_employee.name_related,
                         fleet_vehicle.model_id ,
                         fleet_vehicle_model.name,
                         fleet_vehicle.vehicle_code ,
                         fleet_vehicle.entry_state,
                         hr_employee.workpost,
                         employees_post.name,
                         bus_group.id ,
                         fleet_vehicle.company_id)
                     union
                     (select
                         fleet_vehicle.company_id, 
                         bus_group.route_id as line_id,
                         bus_group.id  as bus_group_id,
                         fleet_vehicle.model_id as bus_model,
                         fleet_vehicle_model.name as bus_model_name,
                         fleet_vehicle.vehicle_code as bus_code,
                         fleet_vehicle.entry_state,
                         hr_employee.workpost as workpsot_id,
                         hr_employee.jobnumber,
                         employees_post.name as workpost_name,
                         hr_employee.name_related as employee_name   
                     from 
                         bus_group_driver_vehicle_shift
                     left join 
                         bus_group on bus_group.id = bus_group_driver_vehicle_shift.group_id
                     left join
                         bus_group_vehicle on bus_group_vehicle.id = bus_group_driver_vehicle_shift.bus_group_vehicle_id    
                     left join
                         fleet_vehicle on bus_group_vehicle.vehicle_id = fleet_vehicle.id
                     left join fleet_vehicle_model on fleet_vehicle_model.id = fleet_vehicle.model_id
                     left join 
                         bus_group_driver on bus_group_driver.id = bus_group_driver_vehicle_shift.driver_id
                     left join 
                         hr_employee on bus_group_driver.driver_id = hr_employee.id
                     left join employees_post on employees_post.id = hr_employee.workpost
                     where   
                        bus_group_driver_vehicle_shift.driver_id is not null and bus_group_driver_vehicle_shift.active = true
                     group by 
                         bus_group.route_id,
                         hr_employee.workpost,
                         hr_employee.jobnumber,
                         hr_employee.name_related,
                         fleet_vehicle.model_id ,
                         fleet_vehicle_model.name,
                         fleet_vehicle.vehicle_code ,
                         fleet_vehicle.entry_state,
                         hr_employee.workpost,
                         employees_post.name,
                         bus_group.id ,
                         fleet_vehicle.company_id
                      order by  hr_employee.name_related)
                    
                    ) driver_conductor
                    
                    where  bus_code is not null and jobnumber is not null and  bus_group_id is not null
                    group by company_id,bus_group_id,line_id,bus_model,bus_model_name,bus_code,entry_state,workpsot_id,jobnumber,employee_name,workpost_name
                    
                    order by employee_name

            )""")
class line_bus_employee_shedule4bus(models.Model):
    _name = 'line.bus.employee.shedule4bus'
    _auto = False
    _order = 'bus_code asc'
    
    id = fields.Char()
    company_id = fields.Many2one('hr.department')
    bus_group_id = fields.Many2one('bus_group')
    line_id = fields.Many2one('route_manage.route_manage')
    bus_model = fields.Many2one('fleet.vehicle.model')
    bus_model_name = fields.Char()
    bus_code = fields.Char()
    entry_state = fields.Char()
    workpost_id = fields.Many2one('employees.post')
    jobnumber = fields.Char()
    employee_name = fields.Char()
    workpost_name = fields.Char()
    conductor_ct = fields.Integer(related='bus_group_id.conductor_ct', readonly=True, string="conductor_ct")
    driver_ct = fields.Integer(related='bus_group_id.driver_ct', readonly=True, string="driver_ct")

    @api.model_cr
    def init(self):
        drop_view_if_exists(self._cr, 'line_bus_employee_shedule4bus')
        self._cr.execute("""
            CREATE OR REPLACE VIEW line_bus_employee_shedule4bus AS (
                select
                     bus_code as id, 
                     company_id,
                     bus_group_id,
                     line_id,
                     bus_model,
                     bus_model_name,
                     bus_code,
                     entry_state
                
                 from line_bus_employee_shedule
                
                
                 group by 
                     company_id,
                     line_id,
                     bus_model,
                     bus_model_name,
                     bus_code,
                     bus_group_id,
                     entry_state        
            )""")                
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
