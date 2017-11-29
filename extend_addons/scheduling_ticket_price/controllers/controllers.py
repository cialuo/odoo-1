# -*- coding: utf-8 -*-
from odoo import http

# class SchedulingTicketPrice(http.Controller):
#     @http.route('/scheduling_ticket_price/scheduling_ticket_price/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scheduling_ticket_price/scheduling_ticket_price/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('scheduling_ticket_price.listing', {
#             'root': '/scheduling_ticket_price/scheduling_ticket_price',
#             'objects': http.request.env['scheduling_ticket_price.scheduling_ticket_price'].search([]),
#         })

#     @http.route('/scheduling_ticket_price/scheduling_ticket_price/objects/<model("scheduling_ticket_price.scheduling_ticket_price"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scheduling_ticket_price.object', {
#             'object': obj
#         })