# -*- coding: utf-8 -*-
from odoo import http
import json

class Terraform(http.Controller):

    ### Hello World
     @http.route('/terraform/terraform/', auth='public', cors='*')
     def index(self, **kw):
         return "Hello, world"

    ### Generic amb field
     @http.route('/terraform/terraform/<model>/<obj>/<field>', auth='public',cors='*', type='json')
     def terraform_field(self, model, obj, field, **kw):
         model = http.request.env[model].sudo().search([('id','=',obj)]).mapped(lambda p: p.read([field])[0])
         return model
    ### Generic amb id
     @http.route('/terraform/terraform/<model>/<obj>', auth='public',cors='*', type='json')
     def terraform_object(self, model, obj, **kw):
         model = http.request.env[model].sudo().search([('id','=',obj)]).mapped(lambda p: p.read()[0])
         return model
    ### Generic diguent el model i criteris de busqueda
     @http.route('/terraform/terraform/<model>', auth='public',cors='*', type='json')
     def terraform_model_filter(self, model, f1,f2,f3 , **kw):
         model = http.request.env[model].sudo().search([(f1,f2,f3)]).mapped(lambda p: p.read()[0])
         return model

    # Per a login
     @http.route('/terraform/terraform/login', auth='public', cors='*', type='json')
     def terraform_model(self, user, password, **kw):
        passs = http.request.env['terraform.player'].sudo().search([('name','=',user)]).mapped(lambda p: p.password)
        if passs[0] == password:
            return {"login":"si"}
        else:
            return {"login":"no"}
    ### per a players passant el id:
     # @http.route('/terraform/terraform/players/<model("terraform.player"):obj>/', auth='public',cors='*')
     # def player(self, obj, **kw):
     #     player = http.request.env['terraform.player'].sudo().search([('id','=',obj.id)]).mapped(lambda p: {'id':p.id, 'name': p.name, 'avatar':str(p.avatar)})
     #     #print(player)
     #     return json.dumps(player)
    ### Per a players passant el id i el field:
     # @http.route('/terraform/terraform/players/<model("terraform.player"):obj>/<field>', auth='public',cors='*')
     # def player_field(self, obj, field, **kw):
     #     player = http.request.env['terraform.player'].sudo().search([('id','=',obj.id)]).mapped(lambda p: {field: str(p[field])})
     #     #print(player)
     #     return json.dumps(player)

     ### planetes en limit. interessamt com passem dirèctament el resultat de read
     # @http.route('/terraform/terraform/planets/<limit>', auth='public', cors='*', type="json", csrf=False )
     # def list(self, limit, **kw):
     #  # https://stackoverflow.com/questions/51149008/odoo-export-res-company-object-to-json
     #     planets = http.request.env['terraform.planet'].sudo().search([],limit=int(limit)).mapped(lambda p: p.read()[0])
     #     #planets = {'planets':planets}
     #     #print(planets)
     #     #planets = json.dumps(planets)
     #     return planets

       #  return http.request.render('terraform.listing', {
       #      'root': '/terraform/terraform',
       #      'objects': http.request.env['terraform.planet'].sudo().search([]),   # Lo del sudo a solucionar con autentificacion
       #  })

     # @http.route('/terraform/terraform/planet/<model("terraform.planet"):obj>/', auth='public',cors='*', type='json', csrf=False)
     # def planet(self, obj, **kw):
     #     print(obj)
     #     planet = http.request.env['terraform.planet'].sudo().search([('id','=',obj.id)]).mapped(lambda p: p.read()[0])
     #     return planet

     # @http.route('/terraform/session/authenticate', auth="none", cors='*', csrf=False, type='json')
     # def authenticate(self, db, login, password, base_location=None):
     #    # print(db,login,password)
     #     http.request.session.authenticate(db, login, password)
     #     print(http.request.env['ir.http'].session_info())
     #     return http.request.env['ir.http'].session_info()

# https://www.odoo.com/es_ES/forum/ayuda-1/question/avoid-cors-error-webapp-cordova-99048
# https://stackoverflow.com/questions/61519072/how-do-i-do-post-get-request-from-ajax-to-odoo-10-custom-module-controller-blo
