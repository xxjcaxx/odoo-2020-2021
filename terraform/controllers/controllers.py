# -*- coding: utf-8 -*-
from odoo import http
import json
from pprint import pprint

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
         records =  http.request.env[model].sudo().search([(f1,f2,f3)])
        # print(model,f1,f2,f3, travel, http.request.env[model].sudo().search([]))
         model = records.mapped(lambda p: p.read()[0])
         return model

         ### Generic diguent el model i criteris de busqueda


     @http.route('/terraform/terraform/name_id/<model>', auth='public', cors='*', type='json')
     def terraform_name_id_filter(self, model, f1, f2, f3, **kw):
        records = http.request.env[model].sudo().search([(f1, f2, f3)])
        # print(model,f1,f2,f3, travel, http.request.env[model].sudo().search([]))
        model = records.mapped(lambda p: p.read(['id','name'])[0])
        return model

    # Per a login
     @http.route('/terraform/terraform/login', auth='public', cors='*', type='json')
     def terraform_model(self, user, password, **kw):
        passs = http.request.env['res.partner'].sudo().search([('name','=',user)])
        if(passs):
            if passs[0].password == password:
                return {"login":"si", "id": passs[0].id}
            else:
                print('no pass')
                return {"login": "no"}
        else:
            print('no user')
            return {"login":"no"}

    # Per a crear coses sense API REST
     @http.route('/terraform/terraform/create/travel', auth='public', cors='*', type='json')
     def terraform_model_create(self, p1, p2, player, **kw):
        travel = http.request.env['terraform.travel'].sudo().create({'origin_planet':p1, 'destiny_planet': p2, 'player':player})
        return travel.read()[0]


     @http.route('/terraform/terraform/<model>/create', auth='public', cors='*', type='json')
     def terraform_model_create(self, model, data, **kw):
        new_id = http.request.env[model].sudo().create(data)
        return new_id.read()[0]

     @http.route('/terraform/session/authenticate', auth="none", cors='*', csrf=False, type='json')
     def authenticate(self, db, login, password, base_location=None):
          print(db,login,password)
          http.request.session.authenticate(db, login, password)
          print(http.request.env['ir.http'].session_info())
          return http.request.env['ir.http'].session_info()

########################### INFORMACIÓ #############################
     @http.route('/terraform/info', auth="none", cors='*', csrf=False, type='json')
     def info(self, user,  password, base_location=None):
       print('infoooooooooooooooooooooooooooooooooooo')
       print(http.request.httprequest.__dict__)
       pprint(http.request.httprequest)
       #help(http.request.httprequest)
       print(http.request.httprequest.method)
       print(http.request.params)
       return http.request.env['ir.http'].session_info()




################################### API REST ##############################3
     @http.route('/terraform/api/<model>', auth="none", cors='*', csrf=False, type='json')
     def api(self, **args):
       print('APIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
       print(args, http.request.httprequest.method)
       model = args['model']
       if( http.request.httprequest.method == 'POST'):   #  {"jsonrpc":"2.0","method":"call","params":{"planet":{"name":"Trantor","average_temperature":20},"password":"1234"}}
           record = http.request.env['terraform.'+model].sudo().create(args[model])
           return record.read()
       if( http.request.httprequest.method == 'GET'):
           record = http.request.env['terraform.'+model].sudo().search([('id','=',args[model]['id'])])
           return record.read()
       if( http.request.httprequest.method == 'PUT' or  http.request.httprequest.method == 'PATCH'):
           record = http.request.env['terraform.'+model].sudo().search([('id','=',args[model]['id'])])[0]
           record.write(args[model])
           return record.read()
       if(http.request.httprequest.method == 'DELETE'):
           record = http.request.env['terraform.'+model].sudo().search([('id','=',args[model]['id'])])[0]
           print(record)
           record.unlink()
           return record.read()

       return http.request.env['ir.http'].session_info()



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


# https://www.odoo.com/es_ES/forum/ayuda-1/question/avoid-cors-error-webapp-cordova-99048
# https://stackoverflow.com/questions/61519072/how-do-i-do-post-get-request-from-ajax-to-odoo-10-custom-module-controller-blo
