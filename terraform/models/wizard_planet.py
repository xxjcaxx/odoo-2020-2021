from odoo import models, fields, api
import random
import string
import json
import math
from datetime import datetime, timedelta

class planet_wizard(models.TransientModel):
    _name = 'terraform.planet_wizard'

    name = fields.Char()
    player = fields.Many2one('res.partner')
    n_planet = fields.Integer(compute='get_n_planet')  # n planet from sun

    def _default_sun(self):
        return self.env['terraform.sun'].browse(self._context.get('active_id'))  # El context conté, entre altre coses,
        # el active_id del model que està obert.
    sun = fields.Many2one('terraform.sun', default=_default_sun, readonly=True)
    image = fields.Image(max_width=200, max_height=200)
    average_temperature = fields.Float()
    oxigen = fields.Float()
    co2 = fields.Float()
    water = fields.Float()
    gravity = fields.Float()
    air_density = fields.Float()
    energy = fields.Float(default=0)

    plants = fields.Float(default=0)  # Percentatge de superficie del planeta en plantes
    animals = fields.Float(default=0)  # Percentatge de superficie del planeta en animals

    buildings = fields.One2many('terraform.building', 'planet')


    #### Fields per al wizard
    state = fields.Selection([('global','Global Data'),
                              ('enviroment','Enviroment'),
                              ('buildings','Buildings')],
                             default='global'
                             )

    @api.depends('sun')
    def get_n_planet(self):
        if self.sun:
            print('************************')
            n_planet = max(self.sun.planets.mapped('n_planet'))+1
            print(n_planet)
