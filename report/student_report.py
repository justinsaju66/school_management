# -*- coding: utf-8 -*-
from datetime import timedelta, datetime


from odoo import  models, api


class StudentReport(models.AbstractModel):
    _name = 'report.school_management.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        query = """
            SELECT student_registration.*, 
                   manage_department.name AS dep_name
                 
            FROM student_registration
            INNER JOIN manage_department 
                ON student_registration.department_id = manage_department.id
            
            WHERE 1=1
        """
        params = []

        if data:
            if data.get('student_id'):
                query += " AND student_registration.id = %s"
                params.append(data['student_id'])

            if data.get('department_id'):
                query += " AND manage_department.name = %s"
                params.append(data['department_id'])

            # if data.get('class_id'):
            #     query += " AND manage_class.name = %s"
            #     params.append(data['class_id'])

        print("Final SQL Query:", query)
        print("Parameters:", params)

        self.env.cr.execute(query, tuple(params))
        docs = self.env.cr.dictfetchall()
        print("Query Results:", docs)

        return {
            'doc_ids': docids,
            'doc_model': 'student.registration',
            'docs': docs,
            'data': data,
        }



