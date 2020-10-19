# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
from odoo.exceptions import ValidationError


class course(models.Model):
     _name = 'school.course'
     _description = 'Courses'

     name = fields.Char()
     students = fields.One2many('school.student', 'course')
     country = fields.Many2one('res.country')
     students_computed = fields.Many2many('school.student',compute='_get_students')

     def _get_students(self):
          for course in self:
               course.students_computed = self.env['school.student'].search([('course','=',course.id)]).ids

     course_start = fields.Datetime(compute='_get_hour')

     def _get_hour(self):
          for c in self:
               c.course_start = fields.datetime.now()


class student(models.Model):
     _name = 'school.student'
     _description = 'Students'

     name = fields.Char()
     def _get_level(self):
          return '2'

     level = fields.Char(default=_get_level)
     age = fields.Integer()
     course = fields.Many2one('school.course')
     course_name = fields.Char(string='Course Name',related='course.name')
     course_country = fields.Char(string='Course country', related='course.country.name')
     aleatori = fields.Char(compute='_compute_aleatori')
     country_computed = fields.Many2one('res.country',compute='_get_country')

     @api.depends('name')
     def _compute_aleatori(self):
          print(self)
          for s in self:
               print(s)
               s.aleatori = str(s.name)+" "+str(random.randint(1,1e6))


     @api.depends('course')
     def _get_country(self):
          for s in self:
               s.country_computed = s.course.country.id

     #def _get_date(self):
      #    return fields.datetime.now()

     matriculacio = fields.Datetime(default=lambda  self: fields.Datetime.now())

     @api.constrains('age')
     def _check_something(self):
          for record in self:
               if record.age > 20:
                    raise ValidationError("Your record is too old: %s" % record.age)