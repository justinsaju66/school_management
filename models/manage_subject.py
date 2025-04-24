# -*- coding: utf-8 -*-

from odoo import fields, models

class ManageSubject(models.Model):
    """Model for manage subject"""
    _name = 'manage.subject'
    _description = 'Manage subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    department_id = fields.Many2one(
        comodel_name='manage.department',
        string="Department",
        )
    max_mark = fields.Integer("Max Mark")
    avg_mark = fields.Integer("Avg Mark")
