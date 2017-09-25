# -*- coding: utf-8 -*-
from odoo import http

# class CheshiOdoo(http.Controller):
#     @http.route('/cheshi_odoo/cheshi_odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cheshi_odoo/cheshi_odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cheshi_odoo.listing', {
#             'root': '/cheshi_odoo/cheshi_odoo',
#             'objects': http.request.env['cheshi_odoo.cheshi_odoo'].search([]),
#         })

#     @http.route('/cheshi_odoo/cheshi_odoo/objects/<model("cheshi_odoo.cheshi_odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cheshi_odoo.object', {
#             'object': obj
#         })