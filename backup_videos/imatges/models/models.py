# -*- coding: utf-8 -*-

from odoo import models, fields, api, modules
import base64

class edifici(models.Model):
    _name = 'imatges.edifici'
    name = fields.Char()

    def _get_default_image(self):
        return self.env.ref('imatges.edifici_1').foto
       # with open(modules.get_module_resource('imatges', 'static/src/img', 'demo.jpg'), 'rb') as f:
       #     img = f.read()
       #     return base64.b64encode(img)

    tipus = fields.Selection([('1','Hotel'),('2','Institut'),('3','Gratacels')],default='1')
    foto = fields.Image(default=_get_default_image, max_width=200, max_height=200)

   # @api.onchange('tipus')
   # def _onchange_tipus(self):
   #     nom_img = 'demo'+str(self.tipus)+'.jpg'
   #     with open(modules.get_module_resource('imatges', 'static/src/img', nom_img), 'rb') as f:
   #         img = f.read()
   #         self.foto =  base64.b64encode(img)

