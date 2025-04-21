from odoo import http
from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route(['/webform_view', '/webform_view/page/<int:page>'], auth='public', website=True)
    def web_form_view(self, page=1, **kwargs):
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

    @route('/webform_view/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        print('hey')
        return request.render('school_management.web_form_template')

    @route('/webform/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        print('hi')
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
        print('hello')
        return request.render('school_management.thank_you_page')

    @http.route('/student/<model("student.registration"):student>/', auth='public', website=True)
    def teacher(self, student):
        return http.request.render('school_management.student_details', {
            'person': student
        })


