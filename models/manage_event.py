# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields, models


class ManageEvent(models.Model):
    """Model for manage event"""

    _name = 'manage.event'
    _description = 'Manage Event'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    club_id = fields.Many2one(
        comodel_name='manage.club',
        string="Club",
        )
    event_date = fields.Date(string="Date")
    school_id = fields.Many2one(
        comodel_name='res.company',
        string="School", default=lambda self: self.env.company,
        )
    active = fields.Boolean(string="Active")
    user_id = fields.Many2one(comodel_name="res.partner")
    photo = fields.Binary(string='Photo')

    def action_send_mail(self):
        """Method for action button and send mail for all partner"""

        employee_id = self.env['res.partner'].search(["|",('school_partner', '=', 'teacher') ,
                                                      ('school_partner', '=', 'office_staff')])
        template_id = self.env.ref('school_management.event_email_template')
        if template_id:
            for employee in employee_id:
                template_id.send_mail(self.id, force_send=True, raise_exception=True,
                    email_values={'email_from': self.user_id.email, 'email_to': employee.email})


    def email_reminder(self):
        """Method for send email two days before event"""
        records = self.search([])
        for rec in records:
            if not rec.event_date:
                return
            two_days = rec.event_date - timedelta(days=2)
            if two_days == fields.Date.today():
                self.action_send_mail()
            else:
                return 0

    def _archive_occurred_event(self):
        """Method for archive event that has occurred"""
        records = self.search([])
        for rec in records:
            if rec.event_date != 0:
                today = fields.Date.today()
                if rec.event_date < today:
                    rec.active = False
                else:
                    rec.active = True

