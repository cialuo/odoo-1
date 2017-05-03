# -*- coding: utf-8 -*-
from odoo import http

# class Revenue(http.Controller):
#     @http.route('/revenue/revenue/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/revenue/revenue/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('revenue.listing', {
#             'root': '/revenue/revenue',
#             'objects': http.request.env['revenue.revenue'].search([]),
#         })

#     @http.route('/revenue/revenue/objects/<model("revenue.revenue"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('revenue.object', {
#             'object': obj
#         })