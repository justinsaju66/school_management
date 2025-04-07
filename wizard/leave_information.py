# -*- coding: utf-8 -*-
from datetime import timedelta

from dateutil.utils import today

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
            'student': self.student_id.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'filter_by':self.filter_by,

        }
        return self.env.ref('school_management.action_report_student_leave').report_action(self, data=data)

class LeaveReport(models.AbstractModel):
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self, docids, data=None):
        query = """
              SELECT * 
            FROM manage_leave
            WHERE 1=1
        """

        params = []
        if data.get('student_id'):
            query += " AND student_id = student_id"
            params.append(data['student_id'])

        self.env.cr.execute(query, tuple(params))
        docs = self.env.cr.dictfetchall()
        print('docs',docs)

        return {
            'doc_ids': docids,
            'doc_model': 'manage.leave',
            'docs': docs,
            'data': data,
        }




