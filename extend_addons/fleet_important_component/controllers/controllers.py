# -*- coding: utf-8 -*-
from odoo import http

# class FleetImportantComponent(http.Controller):
#     @http.route('/fleet_important_component/fleet_important_component/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fleet_important_component/fleet_important_component/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fleet_important_component.listing', {
#             'root': '/fleet_important_component/fleet_important_component',
#             'objects': http.request.env['fleet_important_component.fleet_important_component'].search([]),
#         })

#     @http.route('/fleet_important_component/fleet_important_component/objects/<model("fleet_important_component.fleet_important_component"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fleet_important_component.object', {
#             'object': obj
#         })