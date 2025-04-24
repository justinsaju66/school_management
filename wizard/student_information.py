# -*- coding: utf-8 -*-

import json
from odoo import fields, models
from odoo.tools import json_default

class StudentInformation(models.TransientModel):
    _name = 'student.information'
    _description = 'student Information'

    student_id = fields.Many2one(
        comodel_name='student.registration',
        string="Student")

    class_id = fields.Many2one(
        comodel_name='manage.class',
        string="Class",
        )
    department_id = fields.Many2one(
        comodel_name='manage.department',
        string="Department",
        )
    club_id = fields.Many2one(comodel_name='manage.club')



    def action_report_leave(self):
        """Fetch student data """
        data = {
            'student_id': self.student_id.id,
            'student_name': self.student_id.name,
            'department_id': self.department_id.id,
            'class_id': self.class_id.id,
            'club_id': self.club_id.id,
        }
        return self.env.ref('school_management.action_report_student_information').report_action(self, data=data)

    def action_exl_report_student(self):
        """Fetch student data for excel report"""
        company = self.env.company

        data = {
            'student_id': self.student_id.id,
            'student_name': self.student_id.name,
            'department_id': self.department_id.id,
            'class_id': self.class_id.id,
            'club_id': self.club_id.id,
            'company_name':company.name,
            'company_address':company.street,
            'company_logo':company.logo
        }
        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {
                'model': 'report.school_management.report_student',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Student Excel Report',
                'token': 'file_token_123',
            },
        }
