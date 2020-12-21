# -*- coding: utf-8 -*-

from odoo import models, fields, api

class advanced_building(models.Model):
    _inherits = {'terraform.building': 'building_id'}
    _name = 'terraform.advanced_building'
    _description = 'Advanced Building'

    lab_level = fields.Integer()
