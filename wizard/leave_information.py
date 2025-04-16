# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter
from odoo import fields, models
from odoo.tools import json_default


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
    class_id = fields.Many2one(
        comodel_name='manage.class',
        string="Class")

    def action_report_leave(self):
        """Trigger PDF or QWeb report"""
        data = {
            'student_id': self.student_id.id,
            'student_name': self.student_id.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'class_id': self.class_id.id,
            'filter_by': self.filter_by,
        }
        return self.env.ref('school_management.action_report_student_leave').report_action(self, data=data)

    def action_exl_report_leave(self):
        company = self.env.company
        data = {
            'student_id': self.student_id.id,
            'student_name': self.student_id.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'class_id': self.class_id.id,
            'filter_by': self.filter_by,
            'company_name': company.name,
            'company_address': company.street,
            'company_logo': company.logo
        }
        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {
                'model': 'report.school_management.report_leave',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Leave Excel Report',
                'token': 'file_token_123',
            },
        }


