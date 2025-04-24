# -*- coding: utf-8 -*-

from odoo import fields, models

class ManageClass(models.Model):
    """Model for manage classS"""
    _name = 'manage.class'
    _description = 'Manage class'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    department_id = fields.Many2one(
        comodel_name='manage.department',
        string="Department",
        )
    hod_id = fields.Many2one(related='department_id.hod_id')
    school_id = fields.Many2one(
        comodel_name='res.company',
        string="School", default=lambda self: self.env.user.company_id.id,
        )
