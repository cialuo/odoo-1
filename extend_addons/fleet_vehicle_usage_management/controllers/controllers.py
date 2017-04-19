# -*- coding: utf-8 -*-
from odoo import http

# class FleetVehicleUsageManagement(http.Controller):
#     @http.route('/fleet_vehicle_usage_management/fleet_vehicle_usage_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fleet_vehicle_usage_management/fleet_vehicle_usage_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fleet_vehicle_usage_management.listing', {
#             'root': '/fleet_vehicle_usage_management/fleet_vehicle_usage_management',
#             'objects': http.request.env['fleet_vehicle_usage_management.fleet_vehicle_usage_management'].search([]),
#         })

#     @http.route('/fleet_vehicle_usage_management/fleet_vehicle_usage_management/objects/<model("fleet_vehicle_usage_management.fleet_vehicle_usage_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fleet_vehicle_usage_management.object', {
#             'object': obj
#         })