# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Model for manage Teacher"""
    _inherit = 'res.partner'

    school_partner = fields.Selection(
        string='Partner',
        selection=[('teacher', 'Teacher'), ('office_staff', 'Office Staff'),('student','Student')], required=True)







