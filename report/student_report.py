# -*- coding: utf-8 -*-
import io

import xlsxwriter

from odoo import  models, api,_
from odoo.exceptions import UserError


class StudentReport(models.AbstractModel):
    _name = 'report.school_management.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Method for abstract class"""
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


    def get_xlsx_report(self, data, response):
        """Method for XLSX report"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        # cell_format = workbook.add_format({'font_size': '12px', 'align': 'center'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        date_format = workbook.add_format({'font_size': '10px', 'align': 'center', 'num_format': 'yyyy-mm-dd'})
        bold = workbook.add_format({'bold': True,'font_size': '8px','align': 'center'})
        wrap_format = workbook.add_format({'text_wrap': True, 'font_size': '6px', 'align': 'center',
                                           'bold': True})


        # Write company details to the Excel sheet
        sheet.merge_range('A1:B1', 'Company Details:', wrap_format)
        sheet.merge_range('A2:B2', f"Company Name: {data.get('company_name')}", wrap_format)
        sheet.merge_range('A3:B3', 'Address:', wrap_format)
        sheet.merge_range('A4:B5', f" {data.get('company_address')}", wrap_format)


        sheet.merge_range('B6:M7', 'STUDENT DETAILS', head)

        report_data = self._get_report_values([], data)
        docs = report_data.get('docs', [])
        if data.get('student_id'):
            sheet.merge_range('B8:C8', f"Student: {data.get('student_name')}",bold)
        sheet.merge_range('A9:B9', 'STD ID', bold)
        if not data.get('student_id'):
            sheet.merge_range('C9:D9', 'Student Name', bold)
            sheet.merge_range('E9:F9', 'Class', bold)
            sheet.merge_range('G9:H9', 'Email', bold)
            sheet.merge_range('I9:J9', 'Gender', bold)
            sheet.merge_range('K9:L9', 'Department', bold)
        else:
            sheet.merge_range('C9:D9', 'Class', bold)
            sheet.merge_range('E9:F9', 'Email', bold)
            sheet.merge_range('G9:H9', 'Gender', bold)
            sheet.merge_range('I9:J9', 'Department', bold)

        for row, record in enumerate(docs, start=10):

            sheet.merge_range(f'A{row}:B{row}', record.get('sequence', ''), txt)
            if not data.get('student_id'):
                sheet.merge_range(f'C{row}:D{row}', record.get('name', ''), txt)
                sheet.merge_range(f'E{row}:F{row}', record.get('class_name', ''), txt)
                sheet.merge_range(f'G{row}:H{row}', record.get('email', ''), )
                sheet.merge_range(f'I{row}:J{row}', record.get('gender', ''), txt)
                sheet.merge_range(f'K{row}:L{row}', record.get('dep_name', ''), txt)
            else:
                sheet.merge_range(f'C{row}:D{row}', record.get('class_name', ''), txt)
                sheet.merge_range(f'E{row}:F{row}', record.get('email', ''), txt)
                sheet.merge_range(f'G{row}:H{row}', record.get('gender', ''), txt)
                sheet.merge_range(f'I{row}:J{row}', record.get('dep_name', ''), txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()







