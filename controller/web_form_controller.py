from odoo import http
from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route(['/webform_view', '/webform_view/page/<int:page>'], auth='public', website=True)
    def web_form_view(self, page=1, **kwargs):
        """pagination and view for the student registration"""
        student_obj = request.env['student.registration']
        total_students = student_obj.search_count([])
        page_detail = request.website.pager(
            url='/webform_view',
            total=total_students,
            page=page,
            step=10,
        )
        students =student_obj.sudo().search([], offset=page_detail['offset'], limit=10)
        values = {'students': students,'pager': page_detail}
        return request.render('school_management.student_list_template',values)

    @http.route('/student/<model("student.registration"):student>/', auth='public', website=True)
    def student_details(self, student):
        """To view student details"""
        return http.request.render('school_management.web_form_view_template', {
            'person': student
        })

    @route('/webform_view/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        """student registration form"""
        return request.render('school_management.web_form_template')

    @route('/webform/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        """Validation for aadhaar number and submit button in form"""
        aadhaar = post.get('aadhaar_number')

        existing = request.env['student.registration'].sudo().search([('aadhaar_number', '=', aadhaar)], limit=1)

        if existing:
            values = {
                'error_message': 'A student with this Aadhaar number already exists.',
                'person': post
            }
            return request.render('school_management.web_form_template', values)

        request.env['student.registration'].sudo().create({
            'fname': post.get('fname'),
            'lname': post.get('lname'),
            'father': post.get('father'),
            'mother': post.get('mother'),
            'phone': post.get('phone'),
            'email': post.get('email'),
            'dob': post.get('dob'),
            'age': post.get('age'),
            'aadhaar_number': post.get('aadhaar_number'),
        })
        return request.render('school_management.thank_you_page')






