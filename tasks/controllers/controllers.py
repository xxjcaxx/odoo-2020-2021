# -*- coding: utf-8 -*-
# from odoo import http


# class Tasks(http.Controller):
#     @http.route('/tasks/tasks/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tasks/tasks/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tasks.listing', {
#             'root': '/tasks/tasks',
#             'objects': http.request.env['tasks.tasks'].search([]),
#         })

#     @http.route('/tasks/tasks/objects/<model("tasks.tasks"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tasks.object', {
#             'object': obj
#         })
