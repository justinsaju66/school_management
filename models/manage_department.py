# -*- coding: utf-8 -*-

from odoo import fields, models


class ManageDepartment(models.Model):
    """Model for manage department"""

    _name = 'manage.department'
    _description = "Manage department"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    hod_id = fields.Many2one(
        comodel_name='hr.employee',
        string="HOD",
       )




