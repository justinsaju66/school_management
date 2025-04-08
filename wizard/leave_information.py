# -*- coding: utf-8 -*-

from odoo import fields, models, api


class LeaveInformation(models.TransientModel):
    _name = 'leave.information'
    _description = 'Leave Information'

    student_id = fields.Many2one(
        comodel_name='student.registration',
        string="Student")
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="End Date")
    filter_by = fields.Selection(
        string='Filter By',
        selection=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'),
                   ('year', 'Year')])

    def action_report_leave(self):
        """Fetch leave data based on student """
        data = {
            'student_id': self.student_id.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'filter_by': self.filter_by,
        }
        return self.env.ref('school_management.action_report_student_leave').report_action(self, data=data)
