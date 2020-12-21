# -*- coding: utf-8 -*-

from odoo import models, fields, api
# herència de classe
class player_premium(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _description = 'Player Premium'
    # Main fields
    is_premium = fields.Boolean()

    def assign_random_planet(self):
        for p in self:
            super(player_premium, self).assign_random_planet()

