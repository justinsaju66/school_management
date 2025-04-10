# -*- coding: utf-8 -*-
from datetime import timedelta, datetime


from odoo import  models, api,_
from odoo.exceptions import UserError


class StudentReport(models.AbstractModel):
    _name = 'report.school_management.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        query = """
            SELECT student_registration.*, 
                   manage_department.name AS dep_name, 
                   manage_class.name AS class_name,
                   rel.manage_club_id AS cb_id
            FROM student_registration
            LEFT JOIN manage_department 
                ON student_registration.previous_academic_id = manage_department.id
            LEFT JOIN manage_class 
                ON student_registration.class_id = manage_class.id
            LEFT JOIN manage_club_student_registration_rel rel
                ON student_registration.id = rel.student_registration_id
            WHERE 1=1
        """
        params = []

        if data.get('student_id'):
            query += " AND student_registration.id = %s"
            params.append(data['student_id'])

        if data.get('department_id'):
            query += "AND manage_department.id = %s"
            print(query)
            params.append(data['department_id'])

        if data.get('class_id'):
            query += " AND manage_class.id = %s"
            params.append(data['class_id'])

        if data.get('club_id'):
            query += "AND rel.manage_club_id = %s"
            print(query)
            params.append(data['club_id'])

        print(query)
        self.env.cr.execute(query, tuple(params))
        docs = self.env.cr.dictfetchall()
        print(docs)
        if docs:
            return {
                'doc_ids': docids,
                'doc_model': 'student.registration',
                'docs': docs,
                'data': data,
            }
        else:
            raise UserError(_("""No Data\n"""))







