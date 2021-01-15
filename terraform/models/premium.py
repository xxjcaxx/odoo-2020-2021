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
            planets = super(player_premium, p).assign_random_planet()
            if p.is_premium:
                for planet in planets:
                    planet.write({'oxigen':50,'co2':50,'water':50,'average_temperature':25})

