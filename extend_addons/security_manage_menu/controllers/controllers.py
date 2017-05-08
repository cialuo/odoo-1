# -*- coding: utf-8 -*-
from odoo import http

# class SecurityManageMemu(http.Controller):
#     @http.route('/security_manage_memu/security_manage_memu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/security_manage_memu/security_manage_memu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('security_manage_memu.listing', {
#             'root': '/security_manage_memu/security_manage_memu',
#             'objects': http.request.env['security_manage_memu.security_manage_memu'].search([]),
#         })

#     @http.route('/security_manage_memu/security_manage_memu/objects/<model("security_manage_memu.security_manage_memu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('security_manage_memu.object', {
#             'object': obj
#         })