# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import string
import json


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

    plants = fields.Float(default=0) # Percentatge de superficie del planeta en plantes

    buildings = fields.One2many('terraform.building','planet')

    # Aux fields
    image_small = fields.Image(max_width=50, max_height=50, related='image', string='Image Small', store=True)
    available_buildings = fields.Many2many('terraform.building_type',compute='_get_available_buildings')
    construction_buildings = fields.Many2many('terraform.construction',compute='_get_available_buildings')

    def calculate_production(self):  # En funcio dels edificis es calcula la producció de coses
        for p in self:
            if p.energy >= 0:
                p.write({'energy':0})
                for b in p.buildings:
                    b.produce()
            else:
                consumers = p.buildings.filtered(lambda p: p.name.energy_production < 0)
                for b in consumers:
                    b.write({'people':0})
            if p.player:
                # Si te jugador, el planeta comença a tindre efecte hivernacle i altres coses
                if p.co2 > 50:    # Efecte hivernacle
                    p.write({'average_temperature': p.average_temperature + (p.co2*(10-p.n_planet))*0.00001})
                if p.average_temperature > 20:  # Radiació de la temperatura
                    p.write({'average_temperature': p.average_temperature - (p.average_temperature  * 0.000001)})
                #if p.plants > 1:  # reduccio de co2
                #    p.write({'co2': p.co2 + , 'oxigen':  })
                #if p.plants > 20 and p.water > 20 and co2 > 50# Les plantes creixen soles
                #if p.plants > 20 and p.water < 20 and  oxigen > 90 # possibles incendis masius


    def filter_building(self,b,p):  # Sols mostra els edificis possibles
        requirements = json.loads(b.required_enviroment)
        fit = (float(requirements['min_temp']) <= p.average_temperature < float(requirements['max_temp']) and
                p.oxigen >= float(requirements['min_oxigen']) and
                p.co2 >= float(requirements['min_co2']) and
                p.water >= float(requirements['min_water']) and
                float(requirements['min_gravity']) <= p.gravity < float(requirements['max_gravity']) and
                float(requirements['min_air']) <= p.air_density < float(requirements['max_air']))
        if (b.energy_production + p.energy) < 0:
            fit = False
        return fit


    def _get_available_buildings(self):
        for p in self:
            a_b = self.env['terraform.building_type'].search([]).filtered(lambda b: self.filter_building(b,p))
            print(a_b)
            p.available_buildings = a_b.ids
            c_b = self.env['terraform.construction'].search([('planet','=',p.id)])
            p.construction_buildings = c_b.ids

    def open(self):
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'name': self.name,
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'current',
            }

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
    energy = fields.Float(related='name.energy_production')
    percent_energy = fields.Float(compute='_get_percents')

    def produce(self):
        for b in self:
            b.planet.write({
                'oxigen': b.planet.oxigen + b.name.oxigen_production * b.level,
                'co2': b.planet.co2 + b.name.co2_production * b.level,
                'water': b.planet.water + b.name.water_production * b.level,
                'energy': b.planet.energy + b.name.energy_production * b.level,
                'average_temperature': b.planet.average_temperature + b.name.heat_production * b.level,

            })

    def _get_percents(self):
        for b in self:
            consumers = b.planet.buildings.filtered(lambda p: p.name.energy_production < 0)
            producers = b.planet.buildings.filtered(lambda p: p.name.energy_production >= 0)
            #total_consumption = sum(consumers.mapped('name.energy_production'))
            total_production = sum(producers.mapped(lambda r: r.name.energy_production))
            if total_production != 0:
                b.percent_energy = (b.name.energy_production/total_production)*100
            else:
                b.percent_energy = 0
            #print(producers,total_production)
            #else:
               # b.percent_energy = (b.name.energy_production / total_production) * 100

class building_type(models.Model):
    _name = 'terraform.building_type'
    _description = 'Types of buildings'

    name = fields.Char()
    max_people = fields.Integer(default=0)
    energy_production = fields.Float(default=0)
    oxigen_production = fields.Float(default=0)
    co2_production = fields.Float(default=0)
    water_production = fields.Float(default=0)
    heat_production = fields.Float(default=0)

    time = fields.Float(default=10)
    required_buildings = fields.Many2many('terraform.building_type', relation='required_buildings_many2many', column1='building', column2='required')
    required_enviroment = fields.Char(default='{"min_temp":"-20", "max_temp":"60",'
                                               '"min_oxigen":"50",'
                                              '"min_co2":"50",'
                                              '"min_water":"1",'
                                              '"min_gravity":"1","max_gravity":"20",'
                                              '"min_air":"0.1","max_air":"10"}')

    def build(self):
        for b in self:
            print(self.env.context.get('planet'))
            construction = self.env['terraform.construction'].create({
                'planet':self.env.context.get('planet'),
                'building_type':b.id,
            })

#https://www.odoo.com/fr_FR/forum/aide-1/question/best-way-to-show-json-data-on-odoo-ui-171100


class travel(models.Model):
    _name = 'terraform.travel'
    _description = 'Travel to other planets'

    name = fields.Char(compute='_get_name')
    player = fields.Many2one('terraform.player')
    origin_planet = fields.Many2one('terraform.planet')
    destiny_planet = fields.Many2one('terraform.planet')
    distance = fields.Float(compute='_get_distance')  # Distancia en temps
    percent = fields.Float(compute='_get_distance')
    launch_time = fields.Datetime(default=lambda t: fields.Datetime.now())

    @api.depends('origin_planet','destiny_planet','player')
    def _get_name(self):
        for t in self:
            t.name = str(t.player.name)+" "+str(t.origin_planet.name)+" -> "+str(t.destiny_planet.name)

    @api.depends('origin_planet','destiny_planet')
    def _get_distance(self):
        for t in self:
            t.distance = 100 # calcular
            t.percent = 50.0

class construction(models.Model):
    _name = 'terraform.construction'
    _description = 'Construction of buildings'

    name = fields.Char(compute='_get_name')
    planet = fields.Many2one('terraform.planet')
    building_type = fields.Many2one('terraform.building_type')
    time = fields.Float()
    progress = fields.Float(compute='_get_progress')

    @api.depends('planet','building_type')
    def _get_name(self):
        for c in self:
            c.name = str(c.planet.name)+" "+str(c.building_type.name)

    @api.model
    def create(self,value):
        new_id = super(construction,self).create(value)
        new_id.write({'time':new_id.building_type.time})
        return new_id

    def update_progress(self):
        for c in self:
            if c.time <= 1:
                self.env['terraform.building'].create({'name':c.building_type.id,'planet':c.planet.id})
                c.unlink()
            else:
                c.write({'time':c.time-1})

    @api.depends('time')
    def _get_progress(self):
        for c in self:
            if c.building_type:
                c.progress = 100*(1- c.time/c.building_type.time)
            else:
                c.progress = 0

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
                    'water': random.betavariate(1.1, 5)*100,
                })


class template(models.Model):
    _name = 'terraform.template'
    _description = 'Templates of the game'

    name = fields.Char()
    type = fields.Selection([('1','Player'),('2','Planet')])
    image = fields.Image()


