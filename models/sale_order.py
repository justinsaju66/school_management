# -*- coding: utf-8 -*-

from odoo import fields, models

class SaleOrder(models.Model):
    """Inherit sale order model for adding state admitted"""
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=([('admitted', 'Admitted')]))







