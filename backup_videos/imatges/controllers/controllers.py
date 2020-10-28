# -*- coding: utf-8 -*-
# from odoo import http


# class Imatges(http.Controller):
#     @http.route('/imatges/imatges/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/imatges/imatges/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('imatges.listing', {
#             'root': '/imatges/imatges',
#             'objects': http.request.env['imatges.imatges'].search([]),
#         })

#     @http.route('/imatges/imatges/objects/<model("imatges.imatges"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('imatges.object', {
#             'object': obj
#         })
