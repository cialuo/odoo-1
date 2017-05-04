# -*- coding: utf-8 -*-
from odoo import http

# class SecurityFireSafety(http.Controller):
#     @http.route('/security_fire_safety/security_fire_safety/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/security_fire_safety/security_fire_safety/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('security_fire_safety.listing', {
#             'root': '/security_fire_safety/security_fire_safety',
#             'objects': http.request.env['security_fire_safety.security_fire_safety'].search([]),
#         })

#     @http.route('/security_fire_safety/security_fire_safety/objects/<model("security_fire_safety.security_fire_safety"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('security_fire_safety.object', {
#             'object': obj
#         })