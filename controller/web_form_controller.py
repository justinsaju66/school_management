from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route('/webform_view', auth='public', website=True)
    def web_form_view(self, **kwargs):
        students = request.env['student.registration'].sudo().search([])
        return request.render('school_management.student_list_template',{'students': students})

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
            'aadhaar_number': post.get('aadhaar_number'),

        })
        return request.redirect('/webform_view')
