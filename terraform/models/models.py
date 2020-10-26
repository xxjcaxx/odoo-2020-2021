# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import string


def name_generator():
    letters = list(string.ascii_lowercase)
    first = list(string.ascii_uppercase)
    vocals = ['a','e','i','o','u','y','']
    name = random.choice(first)
    for i in range(0,random.randint(3,5)):
        name = name+random.choice(letters)+random.choice(vocals)
    return name



class player(models.Model):
     _name = 'terraform.player'
     _description = 'Human players'
     # Main fields
     name = fields.Char()
     avatar = fields.Image(max_width=200, max_height=200)
     planets = fields.One2many('terraform.planet','player')

     # Aux fields
     avatar_small = fields.Image(max_width=50, max_height=50, related='avatar', store=True)

     def assign_random_planet(self):
         for p in self:
             planetes = self.env['terraform.planet'].search([('player','=',False)]).ids
             planeta = self.env['terraform.planet'].browse(random.choice(planetes))
             planeta.write({'player':p.id})
             life_support = self.env['terraform.building'].create({
                 'name': self.env.ref('terraform.b_type_life_support').id,
                 'people': self.env.ref('terraform.b_type_life_support').max_people,
                 'planet': planeta.id
             })


class planet(models.Model):
    _name = 'terraform.planet'
    _description = 'Planets to terraform'
    # Main Fields
    name = fields.Char()
    player = fields.Many2one('terraform.player')
    n_planet = fields.Integer() # n planet from sun
    sun = fields.Many2one('terraform.sun', ondelete='cascade')
    image = fields.Image(max_width=200, max_height=200)
    average_temperature = fields.Float()
    oxigen = fields.Float()
    co2 = fields.Float()
    water = fields.Float()
    gravity = fields.Float()
    air_density = fields.Float()
    energy = fields.Float(default=0)
    material = fields.Float(default=0)

    buildings = fields.One2many('terraform.building','planet')

    # Aux fields
    image_small = fields.Image(max_width=50, max_height=50, related='image', store=True)

    def calculate_production(self):
        for p in self:
            if p.energy >= 0:
                for b in p.buildings:
                    b.produce()
            else:
                consumers = p.buildings.filtered(lambda p: p.name.energy_production < 0)
                for b in consumers:
                    b.write({'people':0})


class sun(models.Model):
    _name = 'terraform.sun'
    _description = 'Solar system'
    # Main Fields
    name = fields.Char()
    coordinates = fields.Char()
    planets = fields.One2many('terraform.planet','sun')


class building(models.Model):
    _name = 'terraform.building'
    _description = 'Any Building'

    name = fields.Many2one('terraform.building_type')
    people = fields.Integer()
    max_people = fields.Integer(related='name.max_people')
    planet = fields.Many2one('terraform.planet')
    level = fields.Float(default=1)

    def produce(self):
        for b in self:
            b.planet.write({
                'oxigen': b.planet.oxigen + b.name.oxigen_production * b.level,
                'co2': b.planet.co2 + b.name.co2_production * b.level,
                'water': b.planet.water + b.name.water_production * b.level,
                'energy': b.planet.energy + b.name.energy_production * b.level
            })


class building_type(models.Model):
    _name = 'terraform.building_type'
    _description = 'Types of buildings'

    name = fields.Char()
    max_people = fields.Integer(default=0)
    energy_production = fields.Float(default=0)
    oxigen_production = fields.Float(default=0)
    co2_production = fields.Float(default=0)
    water_production = fields.Float(default=0)
    material = fields.Float(default=100)
    time = fields.Float(default=10)
    required_buildings = fields.Many2many('terraform.building_type', relation='required_buildings_many2many', column1='building', column2='required')
    required_enviroment = fields.Char(default='{"min_temp":"-20", "max_temp":"60",'
                                               '"min_oxigen":"50",'
                                              '"min_co2":"50",'
                                              '"min_water":"1",'
                                              '"min_gravity":"1","max_gravity":"20",'
                                              '"min_air":"0.1","max_air":"10"}')
    ### falta: requisits planetaris
#https://www.odoo.com/fr_FR/forum/aide-1/question/best-way-to-show-json-data-on-odoo-ui-171100

#####################################3333


class settings(models.Model):
    _name = 'terraform.settings'
    _description = 'Setting for the module and the game'

    name = fields.Char(default='Setting')

    def generate_universe(self):
        self.env['terraform.sun'].search([]).unlink();

        for i in range(0,100):
            sun = self.env['terraform.sun'].create({'name':'sun'+str(i),'coordinates':str(i)})
            for j in range(1,random.randint(3,10)):
                images = self.env['terraform.template'].search([('type','=','2')]).mapped('image')
                gravity = random.betavariate(1.5, 1.1)
                self.env['terraform.planet'].create({
                    'name': name_generator(),
                    'n_planet':j,
                    'sun':sun.id,
                    'image': random.choice(images),
                    'average_temperature':random.betavariate(5,5)*(11-j)*20 - 50,
                    'oxigen': random.betavariate(1.2, 1.5) * 100,
                    'co2': random.betavariate(1.2, 1.5) * 100,
                    'gravity': gravity*20,
                    'air_density': random.betavariate(1.1, 1.6)*gravity*10,
                })


class template(models.Model):
    _name = 'terraform.template'
    _description = 'Templates of the game'

    name = fields.Char()
    type = fields.Selection([('1','Player'),('2','Planet')])
    image = fields.Image()