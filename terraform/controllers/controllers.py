# -*- coding: utf-8 -*-
from odoo import http
import json

class Terraform(http.Controller):
     @http.route('/terraform/terraform/', auth='public', cors='*')
     def index(self, **kw):
         return "Hello, world"

     @http.route('/terraform/terraform/planets/', auth='public', cors='*' )
     def list(self, **kw):
      # https://stackoverflow.com/questions/51149008/odoo-export-res-company-object-to-json
         planets = http.request.env['terraform.planet'].sudo().search([]).mapped(lambda p: {'name': p.name,
                                                                                            'sun': p.sun.id,
                                                                                            'player' :p.player.id,
                                                                                            'n_player': p.n_planet,
                                                                                            'average_temperature': p.average_temperature,
                                                                                            'oxigen': p.oxigen,
                                                                                            'co2': p.co2,
                                                                                            'water': p.water,
                                                                                            'gravity': p.gravity,
                                                                                            'air_density': p.air_density,
                                                                                            'material': p.material,
                                                                                            'buildings': p.buildings.ids
                                                                                            })
         #planets = {'planets':planets}
         #print(planets)
         planets = json.dumps(planets)
         return planets

       #  return http.request.render('terraform.listing', {
       #      'root': '/terraform/terraform',
       #      'objects': http.request.env['terraform.planet'].sudo().search([]),   # Lo del sudo a solucionar con autentificacion
       #  })

     @http.route('/terraform/terraform/planets/<model("terraform.planet"):obj>/', auth='public',cors='*')
     def object(self, obj, **kw):
         return http.request.render('terraform.object', {
             'object': obj
         })

    # @http.route('/web/session/authenticate', auth="none", cors='*')
    # def authenticate(self, db, login, password, base_location=None):
    #     request.session.authenticate(db, login, password)
    #     return request.env['ir.http'].session_info()

# https://www.odoo.com/es_ES/forum/ayuda-1/question/avoid-cors-error-webapp-cordova-99048
# https://stackoverflow.com/questions/61519072/how-do-i-do-post-get-request-from-ajax-to-odoo-10-custom-module-controller-blo