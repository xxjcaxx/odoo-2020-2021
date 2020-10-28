# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class MyController(http.Controller):
    @http.route('/school/course/', auth='user', type='json')
    def course(self):
        return {
            'html': """
                <div id="school_banner">
                     <link href="/school/static/src/css/banner.css"
                        rel="stylesheet"> 
                    <h1>Curs</h1>
                    <p>Creació de cursos:</p>
                    <a class="couse_button" type="action" data-reload-on-close="true" role="button" data-method="action_course_wizard" data-model="school.course_wizard">
                    Crear Curs
                </a>
                </div> """
        }
    @http.route('/school/courses/', auth='user', type='json')
    def courses(self):
        payload = http.request.env['school.course'].search([])
        print(payload)
        return {
            'html': str(payload)
        }

    @http.route('/school/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()
