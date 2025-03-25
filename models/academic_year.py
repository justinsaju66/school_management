# -*- coding: utf-8 -*-

from odoo import fields, models

class AcademicYear(models.Model):
    """Model for manage Academic year"""
    _name = 'academic.year'
    _description = 'Academic year'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)