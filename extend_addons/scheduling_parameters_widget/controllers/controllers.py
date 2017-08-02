# -*- coding: utf-8 -*-
from odoo import http

# class SchedulingParametersWidget(http.Controller):
#     @http.route('/scheduling_parameters_widget/scheduling_parameters_widget/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scheduling_parameters_widget/scheduling_parameters_widget/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('scheduling_parameters_widget.listing', {
#             'root': '/scheduling_parameters_widget/scheduling_parameters_widget',
#             'objects': http.request.env['scheduling_parameters_widget.scheduling_parameters_widget'].search([]),
#         })

#     @http.route('/scheduling_parameters_widget/scheduling_parameters_widget/objects/<model("scheduling_parameters_widget.scheduling_parameters_widget"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scheduling_parameters_widget.object', {
#             'object': obj
#         })