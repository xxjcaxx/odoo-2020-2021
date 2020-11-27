# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import string
import json
import math
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class challenge(models.Model):
    _name = 'terraform.challenge'
    _description = 'Player challenges'
    # Main fields
    name = fields.Char()
    start_date = fields.Datetime(default=fields.Datetime.now)
    end_date = fields.Datetime(default=lambda d: fields.Datetime.to_string(datetime.now()+timedelta(hours=48)))
    player_1 = fields.Many2one('terraform.player', required=True, ondelete='restrict')
    player_2 = fields.Many2one('terraform.player', required=True, ondelete='restrict')
    planet_1 = fields.Many2one('terraform.planet', required=True, ondelete='restrict')
    planet_2 = fields.Many2one('terraform.planet', required=True, ondelete='restrict')
    description = fields.Text()
    ### Challenge objective
    target_parameter = fields.Selection([('oxigen','Oxigen'),('co2','CO2'),('water','Water'),('plants','Plants'),('animals','Animals')])
    target_goal = fields.Float()

    #### aux fields
    player_1_avatar = fields.Image(related='player_1.avatar_small')
    player_2_avatar = fields.Image(related='player_2.avatar_small')
    planet_1_image = fields.Image(related='planet_1.image_small')
    planet_2_image = fields.Image(related='planet_2.image_small')

    @api.onchange('player_1')
    def _onchange_player1(self):  # No cal fer el for perquè sempre és en un formulari
        if self.player_2:
            if self.player_1.id == self.player_2.id:
                self.player_1 = False
                return {
                    'warning': {
                                   'title': "Players must be different",
                                   'message': "Player 1 is the same as Player 2",
                               }
                }
        return {
             #   'domain': {'planet_1': [('player', '=', self.player_1.id)],
              #             'player_2': [('id', '!=', self.player_1.id)]},
        }

    @api.onchange('player_2')
    def _onchange_player2(self):  # No cal fer el for perquè sempre és en un formulari
        if self.player_1:
            if self.player_1.id == self.player_2.id:
                self.player_2 = False
                return {
                    'warning': {
                                   'title': "Players must be different",
                                   'message': "Player 1 is the same as Player 2",
                               }
                }
        return {
                'domain': {'planet_2': [('player', '=', self.player_2.id)],
                           'player_1': [('id', '!=', self.player_2.id)]},
        }


    @api.onchange('target_goal')
    def _onchange_goal(self):
        if self.target_goal < 0:
            self.target_goal = 0

    @api.constrains('player_1','player2','planet_1','planet_2')
    def _check_player_planets(self):
        for c in self:
            if c.player_1.id == c.player_2.id:
                raise ValidationError('Players must be different')
            if c.player_1.id != c.planet_1.player.id:
                raise ValidationError('Planet 1 is not from player 1')
            if c.player_2.id != c.planet_2.player.id:
                raise ValidationError('Planet 2 is not from player 2')




