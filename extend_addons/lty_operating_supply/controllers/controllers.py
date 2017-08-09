# -*- coding: utf-8 -*-
from odoo import http

# class LtyOperatingSupply(http.Controller):
#     @http.route('/lty_operating_supply/lty_operating_supply/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lty_operating_supply/lty_operating_supply/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lty_operating_supply.listing', {
#             'root': '/lty_operating_supply/lty_operating_supply',
#             'objects': http.request.env['lty_operating_supply.lty_operating_supply'].search([]),
#         })

#     @http.route('/lty_operating_supply/lty_operating_supply/objects/<model("lty_operating_supply.lty_operating_supply"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lty_operating_supply.object', {
#             'object': obj
#         })