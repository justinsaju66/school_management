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
        report_data = self._get_report_values([], data)
        docs = report_data.get('docs', [])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Leave Report")

        bold = workbook.add_format({'bold': True})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

        headers = ['Student Name', 'Class', 'Leave Reason', 'Start Date', 'End Date', 'Status']
        for col, header in enumerate(headers):
            sheet.write(0, col, header, bold)

        for row, record in enumerate(docs, start=1):
            sheet.merge_range(row, 0, record.get('name', ''))
            # sheet.write(row, 1, record.get('class_name', ''))
            # sheet.write(row, 2, record.get('reason', ''))
            # sheet.write(row, 3, record.get('start_date', ''))
            # sheet.write(row, 4, record.get('end_date', ''))

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()




