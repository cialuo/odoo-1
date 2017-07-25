# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.sql import drop_view_if_exists

class dispatch_line_citycode_ref(models.Model):
    _name = "dispatch.line.citycode.ref"
    _description = "line_citycode"
    _auto = False
    _order = "id"

    id = fields.Char('Id', readonly=True)
    line_id = fields.Many2one('opertation_resources_road', readonly=True)
    line_code = fields.Char('Line Code', readonly=True)
    line_name = fields.Char('Line Name', readonly=True)
    company_id = fields.Many2one('res.company', readonly=True)
    company_citycode = fields.Char('City Code', readonly=True)
    station_start = fields.Char('Station start', readonly=True)
    station_end = fields.Char('Station end', readonly=True)
    direction = fields.Char('Direction', readonly=True)

    @api.model_cr
    def init(self):
        drop_view_if_exists(self._cr, 'dispatch_line_citycode_ref')
        self._cr.execute("""
            create or replace view dispatch_line_citycode_ref as (
           select * from  
          (
             select         
                route_manage_route_manage.id::text || '- up'  as id,
                route_manage_route_manage.id as line_id,
                route_manage_route_manage."gprsId" as line_code,
                route_manage_route_manage."lineName" as line_name,
                hr_department.company_id as company_id,
                res_partner.zip as company_citycode,
                up_start.station_first_name as station_start,
                up_last.station_last_name as station_end,
                cast(up_start.direction as char(4)) as direction
            from 
                route_manage_route_manage
            left join
         (
           select 
              opertation_resources_station_up.route_id,
              opertation_resources_station_up.station_id,
              opertation_resources_station.name as station_first_name,
              'up' as direction
           from 
              opertation_resources_station_up
           left join
               opertation_resources_station on  opertation_resources_station_up.station_id = opertation_resources_station.id
           where opertation_resources_station_up.station_type = 'first_station'
         ) as up_start  
         on up_start.route_id = route_manage_route_manage.id
            left join
         (
           select 
              opertation_resources_station_up.route_id,
              opertation_resources_station_up.station_id,
              opertation_resources_station.name as station_last_name,
              'up' as direction
           from 
              opertation_resources_station_up
           left join
               opertation_resources_station on  opertation_resources_station_up.station_id = opertation_resources_station.id
           where opertation_resources_station_up.station_type = 'last_station'
         ) as up_last  
         on up_last.route_id = route_manage_route_manage.id
         
            left join 
            
                hr_department on route_manage_route_manage.department_id = hr_department.id
            
            left join 
                res_partner on res_partner.company_id = res_partner.id
          ) as up   where up.direction is not null
   union 
   select * from 
      (
         select 
                route_manage_route_manage.id::text || '- down'  as id,
                route_manage_route_manage.id as line_id,
                route_manage_route_manage."gprsId" as line_code,
                route_manage_route_manage."lineName" as line_name,
                hr_department.company_id as company_id,
                res_partner.zip as company_citycode,
                down_start.station_first_name as station_start,
                down_last.station_last_name as station_end,
                cast(down_start.direction as char(4)) as direction
            from 
                route_manage_route_manage
            left join
         (
           select 
              opertation_resources_station_down.route_id,
              opertation_resources_station_down.station_id,
              opertation_resources_station.name as station_first_name,
              'down' as direction
           from 
              opertation_resources_station_down
           left join
               opertation_resources_station on  opertation_resources_station_down.station_id = opertation_resources_station.id
           where opertation_resources_station_down.station_type = 'first_station'
         ) as down_start  
         on down_start.route_id = route_manage_route_manage.id
            left join
         (
           select 
              opertation_resources_station_down.route_id,
              opertation_resources_station_down.station_id,
              opertation_resources_station.name as station_last_name,
              'up' as direction
           from 
              opertation_resources_station_down
           left join
               opertation_resources_station on  opertation_resources_station_down.station_id = opertation_resources_station.id
           where opertation_resources_station_down.station_type = 'last_station'
         ) as down_last  
         on down_last.route_id = route_manage_route_manage.id
         
            left join 
            
                hr_department on route_manage_route_manage.department_id = hr_department.id
            
            left join 
                res_partner on res_partner.company_id = res_partner.id

        ) as down where down.direction is not null
            )""")



