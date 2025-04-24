# -*- coding: utf-8 -*-

from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _



class StudentRegistration(models.Model):
    """Model for manage student registrations"""
    _name = 'student.registration'
    _description = 'Student Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    fname = fields.Char(string="First name", required=True)
    lname = fields.Char(string="Last name")
    name = fields.Char(string='Full Name', compute='_compute_name', store=True)
    father = fields.Char(string="Father")
    mother = fields.Char(string="Mother")
    communication_address = fields.Char(string="Communication address")
    same_as_communication = fields.Boolean(string="Same as Communication address")
    permanent_address = fields.Char(string="Permanent Address ")
    email = fields.Char(string="Email",required=True)
    school_id = fields.Many2one(
        comodel_name='res.company',
        string="School", default=lambda self: self.env.company,
        )
    club_ids = fields.Many2many(comodel_name='manage.club')
    phone = fields.Char(string="Phone")
    dob = fields.Date(string="DOB")
    age = fields.Integer(string="Age", compute="_compute_age")
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')
                   ])
    registration_date = fields.Date(string="Registration date", default=datetime.now())
    photo = fields.Binary(string='Photo')

    previous_academic_id = fields.Many2one(
        comodel_name='manage.department',
        string="Previous academic department",
        )
    previous_class_id = fields.Many2one(comodel_name='manage.class',
                                     string="Previous Class",
                                     )
    tc = fields.Binary(string='TC')
    aadhaar_number = fields.Integer(string="Aadhaar number")
    sequence = fields.Char(string="Sequence", default=lambda self: _('New'), copy=False,
                           help="Reference Number of the Students")
    previous_class_ids = fields.Many2many('manage.class', compute='_compute_previous_class_ids')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('registration', 'Registration'),
    ], string='Status', readonly=True, copy=False,
        tracking=True, default='draft')
    exam_count = fields.Integer("Exam Count", compute="_compute_exam_count")
    exam_count_ids = fields.One2many("manage.exam", inverse_name="class_id")
    exam_ids = fields.Many2many(comodel_name='manage.exam')
    class_id = fields.Many2one(
        comodel_name='manage.class',
        string="Class",
        )
    attendance = fields.Boolean(string="Attendance",default=True,readonly=True)
    date = fields.Date(string="Date", default=datetime.now())

    _sql_constraints = [
        ('uniq_name', 'unique(aadhaar_number)',
         "You Entered Aadhaar number is already exists with this name.Give Aadhaar number must be unique!"),
    ]

    @api.depends('fname', 'lname')
    def _compute_name(self):
        """Methods for compute full name"""
        for partner in self:
            partner.name = f"{partner.fname or ''} {partner.lname or ''}".strip()

    def action_register(self):
        """method for register action"""
        self.write({'state': "registration"})

    def action_draft(self):
        """method for draft action"""
        self.write({
            'state': "draft"
        })



    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new student."""
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('student.sequence')
        return super(StudentRegistration, self).create(vals)

    @api.depends('previous_academic_id')
    def _compute_previous_class_ids(self):
        """Method to select only classes that are in department."""
        all_classes = self.previous_class_id.search([])
        for rec in self:
            if rec.previous_academic_id:
                rec.previous_class_ids = all_classes.filtered(
                    lambda cls: cls.department_id.id == rec.previous_academic_id.id
                ).ids
            else:
                rec.previous_class_ids = all_classes.ids

    @api.depends('dob')
    def _compute_age(self):
        """Method for calculate age based on dob"""
        for record in self:

            if record.dob:
                d1 = record.dob

                d2 = date.today()
                record.age = relativedelta(d2, d1).years
            else:
                record.age = 0


    def _compute_exam_count(self):
        """Method for count the exam"""
        for rec in self:
            rec.exam_count = len(rec.exam_ids)

    def action_exam(self):
        """Method for action exam"""
        return {
            'name': 'name',
            'res_model': 'manage.exam',
            'view_mode': 'list,form',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('student_ids', '=', self.id)],
            'context': {
                # 'active_test':False,
                'default_class_id': self.id
            }

        }




    def update_attendance(self):
        """Method for marking attendance"""
        today = fields.Date.today()
        records = self.search([])
        for rec in records:
            if self.env['manage.leave'].search(["&",('student_id', '=', rec.id),
                                                ('start_date', '<=', today),('end_date', '>=', today)]):
                rec.attendance = False
            else:
                rec.attendance = True


    def action_create_user(self):
        """Method for creating User from student registration"""
        user_vals = {
                'name': self.name,
                'login': self.email,
                'email': self.email,
                'phone': self.phone,
                'school_partner': 'student'

            }
        self.env['res.users'].sudo().create(user_vals)









