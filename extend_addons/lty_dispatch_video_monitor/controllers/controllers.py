# -*- coding: utf-8 -*-
from odoo import http

# class LtyDispatchVideoMonitor(http.Controller):
#     @http.route('/lty_dispatch_video_monitor/lty_dispatch_video_monitor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lty_dispatch_video_monitor/lty_dispatch_video_monitor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lty_dispatch_video_monitor.listing', {
#             'root': '/lty_dispatch_video_monitor/lty_dispatch_video_monitor',
#             'objects': http.request.env['lty_dispatch_video_monitor.lty_dispatch_video_monitor'].search([]),
#         })

#     @http.route('/lty_dispatch_video_monitor/lty_dispatch_video_monitor/objects/<model("lty_dispatch_video_monitor.lty_dispatch_video_monitor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lty_dispatch_video_monitor.object', {
#             'object': obj
#         })