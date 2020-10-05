# -*- coding: utf-8 -*-

from odoo import models, fields, api


class task(models.Model):
    _name = 'tasks.task'
    _description = 'Les tasques'

    name = fields.Char(string="Tasca",required=True)
    date = fields.Datetime()
    done = fields.Boolean()
    photo = fields.Image(max_width=200)
    priority = fields.Selection([('1','Low'),('2','Normal'),('3','High')])
    student = fields.Many2one('tasks.student',ondelete='cascade',required=True)
    group = fields.Many2many(comodel_name='tasks.student',
                             relation='task_student_group',
                             column1='task_id', column2='student_id')
    cor_group = fields.Many2many(comodel_name='tasks.student',
                                 relation ='task_student_cor')

class student(models.Model):
    _name = 'tasks.student'
    _description = 'Estudiants'

    name = fields.Char(required=True)
    tasks = fields.One2many('tasks.task','student')
    group_task = fields.Many2many(comodel_name = 'tasks.task',
                                  relation = 'task_student_group',
                                  column1 = 'student_id', column2 = 'task_id')
    cor_task = fields.Many2many(comodel_name='tasks.task',
                                relation = 'task_student_cor')


