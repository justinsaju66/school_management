# -*- coding: utf-8 -*-

from odoo import fields, models


class StudentInformation(models.TransientModel):
    _name = 'student.information'
    _description = 'student Information'

    student_id = fields.Many2one(
        comodel_name='student.registration',
        string="Student")

    class_id = fields.Many2one(
        comodel_name='manage.class',
        string="Class",
        change_default=True, index=True,
        tracking=1,
        check_company=True)
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
