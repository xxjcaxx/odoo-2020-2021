# -*- coding: utf-8 -*-

from odoo import models, fields, api
import secrets
import logging
import re
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class student(models.Model):
     _name = 'res.partner'
     _inherit = 'res.partner'
     #_description = 'school.student'

     #name = fields.Char(string="Nom", readonly=False, required=True, help='Aquest és el nom')
     birth_year = fields.Integer()
     dni = fields.Char(string='DNI')
     password = fields.Char(default=lambda s: secrets.token_urlsafe(12))
     description = fields.Text()
     enrollment_date = fields.Datetime(default=lambda self: fields.Datetime.now())
     last_login = fields.Datetime()
     is_student = fields.Boolean()
     level = fields.Selection([('1', '1'), ('2', '2')])
     photo = fields.Image(max_width=200, max_height=200)
     classroom = fields.Many2one('school.classroom', ondelete='set null', help='La classe a la que va')
     teachers = fields.Many2many('school.teacher',related='classroom.teachers',readonly=True)
     state = fields.Selection([('1', 'Enrolled'), ('2', 'Student'), ('3', 'Ex-Student')],default='1')
     individual_tasks = fields.One2many('school.individual_task','student')
     groupal_tasks = fields.Many2many('school.groupal_task')
     @api.constrains('dni')
     def _check_dni(self):
         regex = re.compile('[0-9]{8}[a-z]\Z', re.I)
         for s in self:
             if regex.match(s.dni):
                 _logger.info('El DNI fa match')
             else:
                 raise ValidationError('El DNI no val')

     _sql_constraints = [ ('dni_uniq','unique(dni)','El DNI no es pot repetir') ]

     def regenerate_password(self):
         for s in self:
             password = secrets.token_urlsafe(12)
             s.write({'password':password})


     @api.onchange('birth_year')
     def _onchange_byear(self):
         if self.birth_year > 2010:
             self.birth_year = 2000
             return { 'warning' :
                          {'title':'Bad birth year',
                           'message': 'The student is too young',
                           'type':'notification'}
                      }

     @api.onchange('level')
     def _onchange_level(self):
         print(self.level)
         return {
             'domain': {'classroom': [('level', '=', self.level)]},
         }

     def open_student(self):
         for s in self:
             action = self.env.ref('school.action_student_modal').read()[0]
             action['res_id']=s.id
             return action

     @api.model
     def cron(self):
         print(self._name)

     @api.model
     def action_students(self,records):
         #records = self.browse(self._context.get('active_ids'))
         for i in records:
             print(i)

     def proves_parametres(self,array_parametres):
         print('Proves parametres')
         print(self.name)
         print(array_parametres)


class classroom(models.Model):
     _name = 'school.classroom'
     _description = 'Les classes'

     name = fields.Char()
     level = fields.Selection([('1','1'),('2','2')])
     course = fields.Many2one('school.course')
     students = fields.One2many(string='Students',comodel_name='res.partner',inverse_name='classroom')
     teachers = fields.Many2many(comodel_name='school.teacher',
                                 relation='teachers_classrooms',
                                 column1='classroom_id',
                                 column2='teacher_id')
     teachers_ly = fields.Many2many(comodel_name='school.teacher',
                                 relation='teachers_classrooms_ly',
                                 column1='classroom_id',
                                 column2='teacher_id')

     all_teachers = fields.Many2many('school.teacher',compute='_get_teachers')



     def _get_teachers(self):
         for c in self:
             c.all_teachers = c.teachers + c.teachers_ly

class teacher(models.Model):
     _name = 'school.teacher'
     _description = 'Els professors'

     name = fields.Char()
     topic = fields.Char()
     phone = fields.Char()
     classrooms = fields.Many2many('school.classroom',
                                 relation='teachers_classrooms',
                                 column2='classroom_id',
                                 column1='teacher_id')
     classrooms_ly = fields.Many2many('school.classroom',
                                 relation='teachers_classrooms_ly',
                                 column2='classroom_id',
                                 column1='teacher_id')


class seminar(models.Model):
    _name = 'school.seminar'
    _description = 'seminars'
    name = fields.Char()
    date = fields.Datetime()
    finish = fields.Datetime()
    hours = fields.Integer()
    classroom = fields.Many2one('school.classroom')

class task(models.Model):
    _name = 'school.task'
    _description = 'base class for tasks'
    name = fields.Char()
    qualification = fields.Float()


class individual_task(models.Model):
    _name = 'school.individual_task'
    _description = 'one student task'
    _inherits = {'school.task':'task_id'}

    student = fields.Many2one('res.partner', ondelete='cascade')

class groupal_task(models.Model):
    _name = 'school.groupal_task'
    _description = 'many student task'
    _inherits = {'school.task': 'task_id'}

    def _get_default_student(self):
        student = self.browse(self._context.get('current_student'))
        if student:
            print(self._context.get('current_student'))
            return [student.id]
        else:
            return []

    students = fields.Many2many('res.partner', default=_get_default_student)


class course(models.Model):
    _name = 'school.course'
    name = fields.Char()

    classrooms = fields.One2many('school.classroom','course')
    students = fields.Many2many('res.partner')
    enrolled_students = fields.Many2many('res.partner', compute='_get_enrolled')

    def _get_enrolled(self):
        for c in self:
            c.enrolled_students = c.students.filtered(lambda s: len(s.classroom) == 1)


class course_wizard(models.TransientModel):
    _name = 'school.course_wizard'

    state = fields.Selection([('1','Course'),('2','Classrooms'),('3','Students'),('4','Enrollment')],default='1')

    name = fields.Char()

    c_name = fields.Char(string='Classroom Name')
    c_level = fields.Selection([('1', '1'), ('2', '2')],string='Classroom Level')
    classrooms = fields.Many2many('school.classroom_aux')

    s_name = fields.Char(string='Student Name')
    s_birth_year = fields.Integer(string='Student Birth Year')
    s_dni = fields.Char(string='DNI')
    students = fields.Many2many('school.student_aux')


    @api.model
    def action_course_wizard(self):
        action = self.env.ref('school.action_course_wizard').read()[0]
        return action

    def next(self):
        if self.state == '1':
            self.state = '2'
        elif self.state == '2':
            self.state = '3'
        elif self.state == '3':
            self.state = '4'
        return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }
    def previous(self):
        if self.state == '2':
            self.state = '1'
        elif self.state == '3':
            self.state = '2'
        elif self.state == '4':
            self.state = '3'
        return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }

    def add_classroom(self):
        for c in self:
            c.write({'classrooms':[(0,0,{'name':c.c_name,'level':c.c_level})]})
        return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }

    def add_student(self):
        for c in self:
            c.write({'students':[(0,0,{'name':c.s_name,'dni':c.s_dni,'birth_year':c.s_birth_year})]})
        return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }


    def commit(self):
        return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }


    def create_course(self):
        for c in self:
            curs = c.env['school.course'].create({'name': c.name})
            students = []
            for cl in c.classrooms:
                classroom = c.env['school.classroom'].create({'name':cl.name,'course':curs.id,'level':cl.level})
                for st in cl.students:
                    student=c.env['res.partner'].create({'name': st.name,
                                                         'dni': st.dni,
                                                         'birth_year': st.birth_year,
                                                         'is_student':True,
                                                         'classroom': classroom.id
                                                         })
                    students.append(student.id)
            curs.write({'students':[(6,0,students)]})


        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.course',
            'res_id': curs.id,
            'view_mode': 'form',
            'target': 'current',

        }

class classroom_aux(models.TransientModel):
    _name = 'school.classroom_aux'
    name = fields.Char()
    level = fields.Selection([('1', '1'), ('2', '2')])
    students = fields.One2many('school.student_aux','classroom')

class student_aux(models.TransientModel):
    _name = 'school.student_aux'
    name = fields.Char()
    birth_year = fields.Integer()
    dni = fields.Char(string='DNI')
    classroom = fields.Many2one('school.classroom_aux')