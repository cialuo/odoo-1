# -*- coding: utf-8 -*-
from odoo import http

# class StockPickingTypes(http.Controller):
#     @http.route('/stock_picking_types/stock_picking_types/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_types/stock_picking_types/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_types.listing', {
#             'root': '/stock_picking_types/stock_picking_types',
#             'objects': http.request.env['stock_picking_types.stock_picking_types'].search([]),
#         })

#     @http.route('/stock_picking_types/stock_picking_types/objects/<model("stock_picking_types.stock_picking_types"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_types.object', {
#             'object': obj
#         })