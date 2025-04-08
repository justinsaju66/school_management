# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta

from odoo import  models, api


class LeaveReport(models.AbstractModel):
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self, docids, data=None):
        query = """
               SELECT manage_leave.*, student_registration.name AS name
                FROM manage_leave
                INNER JOIN student_registration ON manage_leave.student_id = student_registration.id
                WHERE 1=1

        """
        params = []

        if data.get('student_id'):
            query += " AND manage_leave.student_id = %s"
            print(query)
            params.append(data['student_id'])

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
                query += "AND manage_leave.start_date <= %s AND manage_leave.end_date >= "
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

        return {
            'doc_ids': docids,
            'doc_model': 'manage.leave',
            'docs': docs,
            'data': data,
        }
