# -*- coding: utf-8 -*-
from odoo import http

# class LtyServerAccess(http.Controller):
#     @http.route('/lty_server_access/lty_server_access/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lty_server_access/lty_server_access/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lty_server_access.listing', {
#             'root': '/lty_server_access/lty_server_access',
#             'objects': http.request.env['lty_server_access.lty_server_access'].search([]),
#         })

#     @http.route('/lty_server_access/lty_server_access/objects/<model("lty_server_access.lty_server_access"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lty_server_access.object', {
#             'object': obj
#         })