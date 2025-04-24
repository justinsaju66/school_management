# -*- coding: utf-8 -*-

from odoo import fields, models


class ManageExam(models.Model):
    """Model for manage leave"""
    _name = 'manage.exam'
    _description = 'Manage Exam'



    name = fields.Char("Exam Name",required=True)
    student_ids = fields.Many2many(comodel_name='student.registration')
    class_id = fields.Many2one(
        comodel_name='manage.class',
        string="Class",
        )
    paper_ids = fields.Many2many(comodel_name='manage.subject')


    def action_assign(self):
        """method for action assign """
        self.student_ids = self.env['student.registration'].search([('class_id','=', self.class_id.id)]).ids
