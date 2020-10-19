# -*- coding: utf-8 -*-

from odoo import models, fields, api


class course(models.Model):
     _name = 'school.course'
     _description = 'Courses'

     name = fields.Char()
     students = fields.One2many('school.student', 'course')
     country = fields.Many2one('res.country')


class student(models.Model):
     _name = 'school.student'
     _description = 'Students'

     name = fields.Char()
     course = fields.Many2one('school.course')
     course_name = fields.Char(string='Course Name',related='course.name')
     course_country = fields.Char(string='Course country', related='course.country.name')
