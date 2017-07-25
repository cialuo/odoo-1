# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.sql import drop_view_if_exists

class dispatch_line_citycode_ref(models.Model):
    _name = "dispatch.line.citycode.ref"
    _description = "line_citycode"
    _auto = False
    _order = "id"

    id = fields.Integer('Id', readonly=True)
    line_id = fields.Many2one('opertation_resources_road', readonly=True)
    line_code = fields.Char('Line Code', readonly=True)
    line_name = fields.Char('Line Name', readonly=True)
    company_id = fields.Many2one('res.company', readonly=True)
    company_citycode = fields.Char('City Code', readonly=True)

    @api.model_cr
    def init(self):
        drop_view_if_exists(self._cr, 'dispatch_line_citycode_ref')
        self._cr.execute("""
            create or replace view dispatch_line_citycode_ref as (
            select 
                route_manage_route_manage.id as id,
                route_manage_route_manage.id as line_id,
                route_manage_route_manage."gprsId" as line_code,
                route_manage_route_manage."lineName" as line_name,
                hr_department.company_id as company_id,
                res_partner.zip as company_citycode
            from 
                route_manage_route_manage
            left join 
                hr_department on route_manage_route_manage.department_id = hr_department.id
            
            left join 
                res_partner on res_partner.company_id = res_partner.id
            )""")



