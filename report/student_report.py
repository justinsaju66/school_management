# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta

from odoo import  models, api


class StudentReport(models.AbstractModel):
    _name = 'report.school_management.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        query = """
               SELECT * 
               FROM student_registration
                WHERE 1=1

        """
        params = []
        print('fs')
        if data.get('student_id'):
            query += " AND student_registration.name = %s"
            print(query)
            params.append(data['student_id'])


        self.env.cr.execute(query, tuple(params))
        docs = self.env.cr.dictfetchall()
        print('docs', docs)

        return {
            'doc_ids': docids,
            'doc_model': 'student.registration',
            'docs': docs,
            'data': data,
        }
