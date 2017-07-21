# -*- coding: utf-8 -*-
from odoo import http

# class BusSchedulePlan(http.Controller):
#     @http.route('/bus_schedule_plan/bus_schedule_plan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bus_schedule_plan/bus_schedule_plan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bus_schedule_plan.listing', {
#             'root': '/bus_schedule_plan/bus_schedule_plan',
#             'objects': http.request.env['bus_schedule_plan.bus_schedule_plan'].search([]),
#         })

#     @http.route('/bus_schedule_plan/bus_schedule_plan/objects/<model("bus_schedule_plan.bus_schedule_plan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bus_schedule_plan.object', {
#             'object': obj
#         })