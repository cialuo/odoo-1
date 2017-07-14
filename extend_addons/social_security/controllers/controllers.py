# -*- coding: utf-8 -*-
from odoo import http

# class SocialSecurity(http.Controller):
#     @http.route('/social_security/social_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/social_security/social_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('social_security.listing', {
#             'root': '/social_security/social_security',
#             'objects': http.request.env['social_security.social_security'].search([]),
#         })

#     @http.route('/social_security/social_security/objects/<model("social_security.social_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('social_security.object', {
#             'object': obj
#         })