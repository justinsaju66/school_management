# -*- coding: utf-8 -*-
from odoo import fields, models, api, Command


class PartnerMultiInvoice(models.TransientModel):
    _name = 'leave.information'
    _description = 'Leave information'

    student_id = fields.Many2one(
        comodel_name='student.registration',
        string="Student")
    date_from = fields.Date(String="From Date")
    date_to = fields.Date(String="End Date")

    def action_report_leave(self):
        data = {

            'model_id': self.id,
            'from_date': self.date_from,
            'to_date': self.date_to,
            # 'vehicle_id': self.vehicle_id.id,
            # 'vehicle_name': self.vehicle_id.vehicle_name
        }
        # # docids = self.env['purchase.order'].search([]).ids
        return self.env.ref('school_management.action_report_student_leave').report_action(self,data=data)


class LeaveReport(models.AbstractModel):
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['manage.leave'].search(docids)

        return {
            'doc_ids': docs.ids,
            'doc_model': 'manage.leave',
            'docs': docs,
            'data': data,
        }
