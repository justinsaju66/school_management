# -*- coding: utf-8 -*-
from odoo import http


class SchoolManagement(http.Controller):

    @http.route('/school/school/', auth='public', website=True)
    def index(self, **kw):
        Student = http.request.env['student.registration']
        return http.request.render('school_management.index', {
            'student': Student.search([])
        })
