# -*- coding: utf-8 -*-
import io
from datetime import timedelta, datetime

import xlsxwriter
from dateutil.relativedelta import relativedelta

from odoo import  models, api,_
from odoo.exceptions import UserError

class LeaveReport(models.AbstractModel):
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self, docids, data=None):
        query = """
               SELECT manage_leave.*, student_registration.*,manage_class.name AS class_name
                FROM manage_leave
                INNER JOIN student_registration 
                    ON manage_leave.student_id = student_registration.id
                LEFT JOIN manage_class 
                    ON manage_leave.class_id = manage_class.id
                WHERE 1=1
        """

        params = []

        if data.get('student_id'):
            query += " AND student_registration.id = %s"
            params.append(data['student_id'])

        if data.get('class_id'):
            print(data.get('class_id'))
            query += " AND manage_class.id = %s"
            params.append(data['class_id'])

        if data.get('date_from') and data.get('date_to'):
            query += " AND manage_leave.start_date >= %s AND manage_leave.end_date <= %s"
            params.append(data['date_from'])
            params.append(data['date_to'])

        if data.get('filter_by'):
            filter_by = data.get('filter_by')
            if filter_by == 'day':
                today = datetime.today().date()
                query += " AND manage_leave.start_date <= %s AND manage_leave.end_date >= %s"
                params.append(today)
                params.append(today)

            elif filter_by == 'week':
                today = datetime.today()
                week_start = today - timedelta(days=today.weekday())
                week_end = week_start + timedelta(days=6)
                query += "AND manage_leave.start_date <= %s AND manage_leave.end_date >= %s"
                params.append(week_end.strftime('%Y-%m-%d'))
                params.append(week_start.strftime('%Y-%m-%d'))

            elif filter_by == 'month':
                today = datetime.today()
                month_start = today.replace(day=1)
                next_month = month_start + relativedelta(months=1)
                month_end = next_month.replace(day=1) - timedelta(days=1)
                query += "AND manage_leave.start_date <= %s AND manage_leave.end_date >= %s"
                params.append(month_end.strftime('%Y-%m-%d'))
                params.append(month_start.strftime('%Y-%m-%d'))

            elif filter_by == 'year':
                today = datetime.today()
                year_start = today.replace(month=1, day=1)
                year_end = today.replace(month=12, day=31)
                query += """
                                AND manage_leave.start_date <= %s
                                AND manage_leave.end_date >= %s
                            """
                params.append(year_end.strftime('%Y-%m-%d'))
                params.append(year_start.strftime('%Y-%m-%d'))

        self.env.cr.execute(query, tuple(params))
        docs = self.env.cr.dictfetchall()
        print('docs', docs)
        if docs:
            return {
                'doc_ids': docids,
                'doc_model': 'manage.leave',
                'docs': docs,
                'data': data,
            }
        else:
            raise UserError(_("""No Data\n"""))

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        wrap_format = workbook.add_format({'text_wrap': True, 'font_size': '6px', 'align': 'center',
                                           'bold': True})

        # cell_format = workbook.add_format({'font_size': '12px', 'align': 'center'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        date_format = workbook.add_format({'font_size': '10px', 'align': 'center', 'num_format': 'yyyy-mm-dd'})
        bold = workbook.add_format({'bold': True,'font_size': '8px','align': 'center'})

        sheet.merge_range('A1:B1', 'Company Details:', wrap_format)
        sheet.merge_range('A2:B2', f"Company Name: {data.get('company_name')}", wrap_format)
        sheet.merge_range('A3:B3', 'Address:', wrap_format)
        sheet.merge_range('A4:B5', f" {data.get('company_address')}", wrap_format)

        sheet.merge_range('B6:M7', 'LEAVE REPORT', head)

        report_data = self._get_report_values([], data)
        docs = report_data.get('docs', [])

        # headers = ['Student Name', 'Class', 'Leave Reason', 'Start Date', 'End Date', 'Status']
        # for col, header in enumerate(headers, start=1):
        #     sheet.write(3, col, header, cell_format)
        sheet.merge_range('A9:B9', 'Student Name', bold)
        sheet.merge_range('C9:D9', 'Class', bold)
        sheet.merge_range('E9:F9', 'Leave Reason', bold)
        sheet.merge_range('G9:H9', 'Start Date', bold)
        sheet.merge_range('I9:J9', 'End Date', bold)

        # Add data (using merged ranges like the second code)
        for row, record in enumerate(docs, start=10):
            sheet.merge_range(f'A{row}:B{row}', record.get('name', ''), txt)
            sheet.merge_range(f'C{row}:D{row}', record.get('class_name', ''), txt)
            sheet.merge_range(f'E{row}:F{row}', record.get('reason', ''), txt)
            sheet.merge_range(f'G{row}:H{row}', record.get('start_date', ''), date_format)
            sheet.merge_range(f'I{row}:J{row}', record.get('end_date', ''), date_format)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()




