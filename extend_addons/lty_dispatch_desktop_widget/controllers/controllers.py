# -*- coding: utf-8 -*-
from odoo import http

# class LtyDispatchDesktopWidget(http.Controller):
#     @http.route('/lty_dispatch_desktop_widget/lty_dispatch_desktop_widget/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lty_dispatch_desktop_widget/lty_dispatch_desktop_widget/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lty_dispatch_desktop_widget.listing', {
#             'root': '/lty_dispatch_desktop_widget/lty_dispatch_desktop_widget',
#             'objects': http.request.env['lty_dispatch_desktop_widget.lty_dispatch_desktop_widget'].search([]),
#         })

#     @http.route('/lty_dispatch_desktop_widget/lty_dispatch_desktop_widget/objects/<model("lty_dispatch_desktop_widget.lty_dispatch_desktop_widget"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lty_dispatch_desktop_widget.object', {
#             'object': obj
#         })