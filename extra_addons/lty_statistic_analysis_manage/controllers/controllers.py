# -*- coding: utf-8 -*-
from odoo import http

# class ChupengTest(http.Controller):
#     @http.route('/chupeng_test/chupeng_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/chupeng_test/chupeng_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('chupeng_test.listing', {
#             'root': '/chupeng_test/chupeng_test',
#             'objects': http.request.env['chupeng_test.chupeng_test'].search([]),
#         })

#     @http.route('/chupeng_test/chupeng_test/objects/<model("chupeng_test.chupeng_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('chupeng_test.object', {
#             'object': obj
#         })