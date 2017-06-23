# -*- coding: utf-8 -*-
from odoo import http

# class PerformanceAssessment(http.Controller):
#     @http.route('/performance_assessment/performance_assessment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/performance_assessment/performance_assessment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('performance_assessment.listing', {
#             'root': '/performance_assessment/performance_assessment',
#             'objects': http.request.env['performance_assessment.performance_assessment'].search([]),
#         })

#     @http.route('/performance_assessment/performance_assessment/objects/<model("performance_assessment.performance_assessment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('performance_assessment.object', {
#             'object': obj
#         })