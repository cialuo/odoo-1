# -*- coding: utf-8 -*-
from odoo import http

# class LtyAdvancedWorkflow(http.Controller):
#     @http.route('/lty_advanced_workflow/lty_advanced_workflow/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lty_advanced_workflow/lty_advanced_workflow/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lty_advanced_workflow.listing', {
#             'root': '/lty_advanced_workflow/lty_advanced_workflow',
#             'objects': http.request.env['lty_advanced_workflow.lty_advanced_workflow'].search([]),
#         })

#     @http.route('/lty_advanced_workflow/lty_advanced_workflow/objects/<model("lty_advanced_workflow.lty_advanced_workflow"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lty_advanced_workflow.object', {
#             'object': obj
#         })