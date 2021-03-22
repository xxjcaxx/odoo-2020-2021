# -*- coding: utf-8 -*-
# from odoo import http


# class Simulator(http.Controller):
#     @http.route('/simulator/simulator/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/simulator/simulator/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('simulator.listing', {
#             'root': '/simulator/simulator',
#             'objects': http.request.env['simulator.simulator'].search([]),
#         })

#     @http.route('/simulator/simulator/objects/<model("simulator.simulator"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('simulator.object', {
#             'object': obj
#         })
