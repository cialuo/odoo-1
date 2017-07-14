# -*- coding: utf-8 -*-
from odoo import http

# class SecurityManageMemu(http.Controller):
#     @http.route('/security_manage_menu/security_manage_menu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/security_manage_menu/security_manage_menu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('security_manage_menu.listing', {
#             'root': '/security_manage_menu/security_manage_menu',
#             'objects': http.request.env['security_manage_menu.security_manage_menu'].search([]),
#         })

#     @http.route('/security_manage_menu/security_manage_menu/objects/<model("security_manage_menu.security_manage_menu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('security_manage_menu.object', {
#             'object': obj
#         })