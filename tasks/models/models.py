# -*- coding: utf-8 -*-

from odoo import models, fields, api


class task(models.Model):
    _name = 'tasks.task'
    _description = 'Les tasques'

    name = fields.Char()
    date = fields.Datetime()
    done = fields.Boolean()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
