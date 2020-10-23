# -*- coding: utf-8 -*-
# from odoo import http


# class Terraform(http.Controller):
#     @http.route('/terraform/terraform/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/terraform/terraform/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('terraform.listing', {
#             'root': '/terraform/terraform',
#             'objects': http.request.env['terraform.terraform'].search([]),
#         })

#     @http.route('/terraform/terraform/objects/<model("terraform.terraform"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('terraform.object', {
#             'object': obj
#         })
