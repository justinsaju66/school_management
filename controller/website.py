from odoo.http import request, Controller, route

class WebFormController(Controller):
    @route('/webform', auth='public', website=True)
    def web_form(self, **kwargs):
        print('hey')
        return request.render('school_management.web_form_template')
    @route('/webform/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        print('hi')
        request.env['student.registration'].sudo().create({
                    'fname': post.get('fname'),
                    'phone': post.get('phone'),
                    'email': post.get('email'),
                    'aadhaar_number': post.get('aadhaar_number'),
                    'attendance': post.get('attendance'),
                })
        return request.redirect('/thank-you-page')


