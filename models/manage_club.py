# -*- coding: utf-8 -*-

from odoo import fields, models

class ManageClub(models.Model):
    """Model for manage club"""
    _name = 'manage.club'
    _description = 'Manage club'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    student_ids = fields.Many2many(comodel_name='student.registration',ondelete='cascade',)
    event_count = fields.Integer("Event Count", compute ="_compute_event_count")
    event_ids = fields.One2many("manage.event", inverse_name="club_id")

    def _compute_event_count(self):
        """Method for compute event count"""
        for rec in self:
            rec.event_count = len(rec.event_ids)

    def action_event(self):
        """Action for the button event"""
        return {
            'name':'name',
            'res_model': 'manage.event',
            'view_mode': 'list,form',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('club_id', '=', self.id)],
            'context' : {
                # 'active_test':False,
                'default_club_id': self.id
            }
        }