# -*- coding: utf-8 -*-
from odoo import http

# class SecurityRepairProduce(http.Controller):
#     @http.route('/security_repair_produce/security_repair_produce/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/security_repair_produce/security_repair_produce/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('security_repair_produce.listing', {
#             'root': '/security_repair_produce/security_repair_produce',
#             'objects': http.request.env['security_repair_produce.security_repair_produce'].search([]),
#         })

#     @http.route('/security_repair_produce/security_repair_produce/objects/<model("security_repair_produce.security_repair_produce"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('security_repair_produce.object', {
#             'object': obj
#         })