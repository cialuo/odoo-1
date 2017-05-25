# -*- coding: utf-8 -*-
from odoo import http

# class SalaryManage(http.Controller):
#     @http.route('/salary_manage/salary_manage/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salary_manage/salary_manage/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('salary_manage.listing', {
#             'root': '/salary_manage/salary_manage',
#             'objects': http.request.env['salary_manage.salary_manage'].search([]),
#         })

#     @http.route('/salary_manage/salary_manage/objects/<model("salary_manage.salary_manage"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salary_manage.object', {
#             'object': obj
#         })