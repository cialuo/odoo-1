# -*- coding: utf-8 -*-
from odoo import http

# class SecurityVehicleCheck(http.Controller):
#     @http.route('/security_vehicle_check/security_vehicle_check/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/security_vehicle_check/security_vehicle_check/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('security_vehicle_check.listing', {
#             'root': '/security_vehicle_check/security_vehicle_check',
#             'objects': http.request.env['security_vehicle_check.security_vehicle_check'].search([]),
#         })

#     @http.route('/security_vehicle_check/security_vehicle_check/objects/<model("security_vehicle_check.security_vehicle_check"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('security_vehicle_check.object', {
#             'object': obj
#         })