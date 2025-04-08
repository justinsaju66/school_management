# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StudentInformation(models.TransientModel):
    _name = 'student.information'
    _description = 'student Information'

    student_id = fields.Many2one(
        comodel_name='student.registration',
        string="Student")
    filter_by = fields.Selection(
        string='Filter By',
        selection=[('class', 'Class'), ('department', 'Department'), ('club', 'Club')])

    def action_report_leave(self):
        """Fetch student data """
        data = {
            'student_id': self.student_id.id,
            'filter_by': self.filter_by,
        }
        return self.env.ref('school_management.action_report_student_information').report_action(self, data=data)
