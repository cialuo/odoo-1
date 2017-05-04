# -*- coding: utf-8 -*-
from odoo import http

# class SchedulingParameters(http.Controller):
#     @http.route('/scheduling_parameters/scheduling_parameters/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scheduling_parameters/scheduling_parameters/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('scheduling_parameters.listing', {
#             'root': '/scheduling_parameters/scheduling_parameters',
#             'objects': http.request.env['scheduling_parameters.scheduling_parameters'].search([]),
#         })

#     @http.route('/scheduling_parameters/scheduling_parameters/objects/<model("scheduling_parameters.scheduling_parameters"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scheduling_parameters.object', {
#             'object': obj
#         })