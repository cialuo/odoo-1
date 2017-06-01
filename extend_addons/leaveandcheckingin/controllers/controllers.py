# -*- coding: utf-8 -*-
from odoo import http

# class Leaveandcheckingin(http.Controller):
#     @http.route('/leaveandcheckingin/leaveandcheckingin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/leaveandcheckingin/leaveandcheckingin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('leaveandcheckingin.listing', {
#             'root': '/leaveandcheckingin/leaveandcheckingin',
#             'objects': http.request.env['leaveandcheckingin.leaveandcheckingin'].search([]),
#         })

#     @http.route('/leaveandcheckingin/leaveandcheckingin/objects/<model("leaveandcheckingin.leaveandcheckingin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('leaveandcheckingin.object', {
#             'object': obj
#         })