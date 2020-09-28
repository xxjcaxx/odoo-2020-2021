# -*- coding: utf-8 -*-

from odoo import models, fields, api


class couse(models.Model):
     _name = 'school.course'
     _description = 'Courses'

     name = fields.Char()

