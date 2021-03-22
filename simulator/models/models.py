# -*- coding: utf-8 -*-

from odoo import models, fields, api


class simulator(models.Model):
    # un simulador representa a un cron que s'executarà cada cert temps per simular un esdeveniment en l'empresa

     _name = 'simulator.simulator'
     _description = 'Base class for the simulator'

     name = fields.Char()
     type = fields.Selection([('sales','Sales'),('purchases','Purchases')])
     average_period = fields.Integer(default=5)
     cron = fields.Many2one('ir.cron',readonly=True)

     @api.model
     def simular(self):
         print('simular')


     @api.model
     def create(self, values):
        record = super(simulator, self).create(values)
        cron = self.env['ir.cron'].create({
            'name': record.name,
            'model_id': self.env.ref('simulator.model_simulator_simulator').id,
            'state': 'code',
            'code': 'model.run_simulation('+str(record.id)+')',
            'user_id': self.env.ref('base.user_root').id,
            'interval_number': 1,
            'interval_type': 'minutes',
            'numbercall': -1,
            'activity_user_type': 'specific',
            'doall': False
             })
        record.write({'cron': cron.id})
        return record

     def unlink(self):
         print('**************************'+str(self))
         self.cron.unlink()
         return super(simulator,self).unlink()

     @api.model
     def run_simulation(self,id):
         print("Simulation "+str(id))

