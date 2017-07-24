# -*- coding: utf-8 -*-
from odoo import http

# class LtyDispatchDesktopBase(http.Controller):
#     @http.route('/lty_dispatch_desktop_base/lty_dispatch_desktop_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lty_dispatch_desktop_base/lty_dispatch_desktop_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lty_dispatch_desktop_base.listing', {
#             'root': '/lty_dispatch_desktop_base/lty_dispatch_desktop_base',
#             'objects': http.request.env['lty_dispatch_desktop_base.lty_dispatch_desktop_base'].search([]),
#         })

#     @http.route('/lty_dispatch_desktop_base/lty_dispatch_desktop_base/objects/<model("lty_dispatch_desktop_base.lty_dispatch_desktop_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lty_dispatch_desktop_base.object', {
#             'object': obj
#         })