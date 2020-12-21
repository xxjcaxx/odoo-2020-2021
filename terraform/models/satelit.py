# -*- coding: utf-8 -*-

from odoo import models, fields, api

# herència per prototip

class satelit(models.Model):
    _inherit = 'terraform.planet'
    _name = 'terraform.satelit'
    _description = 'Satelit to terraform'

    planet = fields.Many2one('terraform.planet')