# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ManageLeave(models.Model):
    """Model for manage leave"""
    _name = 'manage.leave'
    _description = 'Leaves'
    _rec_name = 'student_id'

    student_id = fields.Many2one(comodel_name='student.registration', string="Student", required=True)
    class_id = fields.Many2one(related='student_id.class_id',store=True)
    start_date = fields.Date(string="Start Date",default=datetime.now())
    end_date = fields.Date(string="End Date")
    total_day = fields.Integer(string="Total Days", compute="_compute_total_day", store=True)
    half_day = fields.Boolean(string="Half Days")
    reason = fields.Char(string="Reason")

    # @api.onchange('start_date', 'end_date', 'total_day')
    # def calculate_date(self):
    #     if self.start_date and self.end_date:
    #         d1 = datetime.strptime(str(self.start_date), '%Y-%m-%d')
    #         d2 = datetime.strptime(str(self.end_date), '%Y-%m-%d')
    #         d3 = d2 - d1
    #         self.total_day = str(d3.days)


    @api.depends("start_date", "end_date")
    def _compute_total_day(self):
        """Method for compute number of leave without include sun and sat"""

        for record in self:
            if record.start_date and record.end_date and record.start_date <= record.end_date:
                days = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}

                dt = record.start_date
                total_days = 0

                while dt <= record.end_date:
                    if dt.weekday() != days['sat'] and dt.weekday() != days['sun']:
                        total_days += 1
                    dt += timedelta(days=1)
                record.total_day = total_days

    @api.constrains('start_date')
    def _check_start_date(self):
        """Method for date selection validation"""

        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError('start date cannot be in past')







