# -*- coding: utf-8 -*-
from odoo import http

# class EmployeesMenu(http.Controller):
#     @http.route('/employees_menu/employees_menu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employees_menu/employees_menu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employees_menu.listing', {
#             'root': '/employees_menu/employees_menu',
#             'objects': http.request.env['employees_menu.employees_menu'].search([]),
#         })

#     @http.route('/employees_menu/employees_menu/objects/<model("employees_menu.employees_menu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employees_menu.object', {
#             'object': obj
#         })