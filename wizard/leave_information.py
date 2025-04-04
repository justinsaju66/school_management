# -*- coding: utf-8 -*-
from odoo import fields, models, api, Command


class LeaveInformation(models.TransientModel):
    _name = 'leave.information'
    _description = 'Leave information'

    student_id = fields.Many2one(
        comodel_name='student.registration',
        string="Student")
    date_from = fields.Date(String="From Date")
    date_to = fields.Date(String="End Date")


    def action_report_leave(self):
        student = self.student_id.ensure_one()
        query = """
                    SELECT *
                    FROM manage_leave
                    INNER JOIN student_registration
                    ON manage_leave.student_id = student_registration.id
                    WHERE manage_leave.student_id = %s
                """
        params = (self.student_id.id,)
        self.env.cr.execute(query ,params)
        report = self.env.cr.dictfetchall()

        data = {
            'student_id': student.name,
            # 'filter_by': self.filter_by,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'report': report,
        }

        return self.env.ref('school_management.action_report_student_leave').report_action(self,data=data)

class LeaveReport(models.AbstractModel):
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('student'):
            domain.append(('student_id', '=', data.get('student')))
        docs = self.env['manage.leave'].search(domain)
        student = self.env['student.registration'].browse(data.get('student'))
        data.update({'student_id': student.name})
        print(data)
        print(docs)

        return {
            'doc_ids': docids,
            'doc_model': 'manage.leave',
            'docs': docs,
            'data': data,
        }
