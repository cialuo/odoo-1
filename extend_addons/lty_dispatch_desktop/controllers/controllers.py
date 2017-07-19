# -*- coding: utf-8 -*-
from odoo import http

# class LtyDispatchDesktop(http.Controller):
#     @http.route('/lty_dispatch_desktop/lty_dispatch_desktop/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lty_dispatch_desktop/lty_dispatch_desktop/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lty_dispatch_desktop.listing', {
#             'root': '/lty_dispatch_desktop/lty_dispatch_desktop',
#             'objects': http.request.env['lty_dispatch_desktop.lty_dispatch_desktop'].search([]),
#         })

#     @http.route('/lty_dispatch_desktop/lty_dispatch_desktop/objects/<model("lty_dispatch_desktop.lty_dispatch_desktop"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lty_dispatch_desktop.object', {
#             'object': obj
#         })