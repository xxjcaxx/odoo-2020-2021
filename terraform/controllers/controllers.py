# -*- coding: utf-8 -*-
from odoo import http
import json

class Terraform(http.Controller):
     @http.route('/terraform/terraform/', auth='public', cors='*')
     def index(self, **kw):
         return "Hello, world"


     @http.route('/terraform/terraform/<model>/<obj>/<field>', auth='public',cors='*', type='json')
     def terraform_field(self, model, obj, field, **kw):
         model = http.request.env[model].sudo().search([('id','=',obj)]).mapped(lambda p: p.read([field])[0])
         return model

     @http.route('/terraform/terraform/<model>/<obj>', auth='public',cors='*', type='json')
     def terraform_object(self, model, obj, **kw):
         print(obj+"**************************")
         model = http.request.env[model].sudo().search([('id','=',obj)]).mapped(lambda p: p.read()[0])
         return model

     @http.route('/terraform/terraform/<model>', auth='public',cors='*', type='json')
     def terraform_model(self, model, **kw):
         model = http.request.env[model].sudo().search([]).mapped(lambda p: p.read()[0])
         return model

     @http.route('/terraform/terraform/players/<model("terraform.player"):obj>/', auth='public',cors='*')
     def player(self, obj, **kw):
         player = http.request.env['terraform.player'].sudo().search([('id','=',obj.id)]).mapped(lambda p: {'id':p.id, 'name': p.name, 'avatar':str(p.avatar)})
         #print(player)
         return json.dumps(player)

     @http.route('/terraform/terraform/players/<model("terraform.player"):obj>/<field>', auth='public',cors='*')
     def player_field(self, obj, field, **kw):
         player = http.request.env['terraform.player'].sudo().search([('id','=',obj.id)]).mapped(lambda p: {field: str(p[field])})
         #print(player)
         return json.dumps(player)

     @http.route('/terraform/terraform/planets/<limit>', auth='public', cors='*', type="json", csrf=False )
     def list(self, limit, **kw):
      # https://stackoverflow.com/questions/51149008/odoo-export-res-company-object-to-json
         planets = http.request.env['terraform.planet'].sudo().search([],limit=int(limit)).mapped(lambda p: p.read()[0]) 
         #planets = {'planets':planets}
         #print(planets)
         #planets = json.dumps(planets)
         return planets

       #  return http.request.render('terraform.listing', {
       #      'root': '/terraform/terraform',
       #      'objects': http.request.env['terraform.planet'].sudo().search([]),   # Lo del sudo a solucionar con autentificacion
       #  })

     @http.route('/terraform/terraform/planet/<model("terraform.planet"):obj>/', auth='public',cors='*', type='json', csrf=False)
     def planet(self, obj, **kw):
         print(obj)
         planet = http.request.env['terraform.planet'].sudo().search([('id','=',obj.id)]).mapped(lambda p: p.read()[0])
         return planet

    # @http.route('/web/session/authenticate', auth="none", cors='*')
    # def authenticate(self, db, login, password, base_location=None):
    #     request.session.authenticate(db, login, password)
    #     return request.env['ir.http'].session_info()

# https://www.odoo.com/es_ES/forum/ayuda-1/question/avoid-cors-error-webapp-cordova-99048
# https://stackoverflow.com/questions/61519072/how-do-i-do-post-get-request-from-ajax-to-odoo-10-custom-module-controller-blo
