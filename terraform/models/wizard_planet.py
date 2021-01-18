from odoo import models, fields, api
import random
import string
import json
import math
from datetime import datetime, timedelta

class planet_wizard(models.TransientModel):
    _name = 'terraform.planet_wizard'

    name = fields.Char(required=True)
    player = fields.Many2one('res.partner', domain="[('is_player', '=', True)]")
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

    buildings = fields.Many2many('terraform.building_type_wizard', compute='_get_buildings')
    def _get_buildings(self):
        building_types = self.env['terraform.building_type'].search([]).mapped(
            lambda bt: self.env['terraform.building_type_wizard'].create({'building_type':bt.id}))
        self.buildings = building_types

    buildings_aux = fields.Many2one('terraform.building_type')
    buildings_new = fields.One2many('terraform.building_wizard','planet_wizard')


    #### Fields per al wizard
    state = fields.Selection([('global','Global Data'),
                              ('enviroment','Enviroment'),
                              ('buildings','Buildings')],
                             default='global'
                             )
    images_template = fields.Many2one('terraform.template')

    @api.depends('sun')
    def get_n_planet(self):
        if self.sun:
            n_planet = max(self.sun.planets.mapped('n_planet'))+1
            self.n_planet = n_planet

    @api.onchange('images_template')
    def onchange_template(self):
        img = self.images_template.image
        self.image = img
        print(img)

    @api.onchange('name')
    def onchange_name(self):
        name = self.name
        if len(self.env['terraform.planet'].search([('name','=',name)])) > 0:
            self.name = name+"_new"
            return({'warning': {'title': "Name Repeated", 'message': "The name is repeated", 'type': 'notification'},})


    def add_building(self):
        b = self.env['terraform.building_wizard'].create({'name': self.buildings_aux.id,'planet_wizard':self.id})
        return {
            'name': "Planet Wizard",
            'view_type': 'form',
            'view_mode': 'form',  # Pot ser form, tree, kanban...
            'res_model': 'terraform.planet_wizard',  # El model de destí
            'res_id': self.id,  # El id concret per obrir el form
            # 'view_id': self.ref('wizards.reserves_form') # Opcional si hi ha més d'una vista posible.
            'context': self._context,  # El context es pot ampliar per afegir opcions
            'type': 'ir.actions.act_window',
            'target': 'new',  # Si ho fem en current, canvia la finestra actual.
        }

    def next(self):
        if self.state == 'global':
            self.state = 'enviroment'
        elif self.state == 'enviroment':
            self.state = 'buildings'
        return {
                'name': "Planet Wizard",
                'view_type': 'form',
                'view_mode': 'form',  # Pot ser form, tree, kanban...
                'res_model': 'terraform.planet_wizard',  # El model de destí
                'res_id': self.id,  # El id concret per obrir el form
                # 'view_id': self.ref('wizards.reserves_form') # Opcional si hi ha més d'una vista posible.
                'context': self._context,  # El context es pot ampliar per afegir opcions
                'type': 'ir.actions.act_window',
                'target': 'new',  # Si ho fem en current, canvia la finestra actual.
            }
    def previous(self):
        if self.state == 'buildings':
            self.state = 'enviroment'
        elif self.state == 'enviroment':
            self.state = 'global'
        return {
                'name': "Planet Wizard",
                'view_type': 'form',
                'view_mode': 'form',  # Pot ser form, tree, kanban...
                'res_model': 'terraform.planet_wizard',  # El model de destí
                'res_id': self.id,  # El id concret per obrir el form
                # 'view_id': self.ref('wizards.reserves_form') # Opcional si hi ha més d'una vista posible.
                'context': self._context,  # El context es pot ampliar per afegir opcions
                'type': 'ir.actions.act_window',
                'target': 'new',  # Si ho fem en current, canvia la finestra actual.
            }

    def create_planet(self):
        new_planet = {}
        new_planet['name'] = self.name
        new_planet['player'] = self.player.id
        new_planet['image'] = self.image
        new_planet['n_planet'] = self.n_planet
        new_planet['sun'] = self.sun.id
        new_planet['average_temperature'] = self.average_temperature
        new_planet['oxigen'] = self.oxigen
        new_planet['co2'] = self.co2
        new_planet['water'] = self.water
        new_planet['gravity'] = self.gravity
        new_planet['air_density'] = self.air_density
        new_planet['energy'] = self.energy

        plants = fields.Float(default=0)  # Percentatge de superficie del planeta en plantes
        animals = fields.Float(default=0)

        planet = self.env['terraform.planet'].create(new_planet)

        for b in self.buildings:
            new_building = self.env['terraform.building'].create({
                'planet': planet.id,
                'name': b.id,
            })

        return {
            'name': 'New Planet',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'terraform.planet',
            'res_id': planet.id,
            'context': self._context,
            'type': 'ir.actions.act_window',
            'target': 'current',
                 }


class building_wizard(models.TransientModel):
    _name = 'terraform.building_wizard'

    name = fields.Many2one('terraform.building_type')
    planet_wizard = fields.Many2one('terraform.planet_wizard')

class building_type_wizard(models.TransientModel):
    _name = 'terraform.building_type_wizard'

    building_type = fields.Many2one('terraform.building_type')
    name = fields.Char(related='building_type.name')

    def add(self):
        planet_wizard = self.env.context.get('planet_wizard')
        b = self.env['terraform.building_wizard'].create({'name': self.building_type.id,
                                                          'planet_wizard':planet_wizard})
        return {
                    'name': "Planet Wizard",
                    'view_type': 'form',
                    'view_mode': 'form',  # Pot ser form, tree, kanban...
                    'res_model': 'terraform.planet_wizard',  # El model de destí
                    'res_id': planet_wizard,  # El id concret per obrir el form
                    # 'view_id': self.ref('wizards.reserves_form') # Opcional si hi ha més d'una vista posible.
                    'context': self._context,  # El context es pot ampliar per afegir opcions
                    'type': 'ir.actions.act_window',
                    'target': 'new',  # Si ho fem en current, canvia la finestra actual.
                }
