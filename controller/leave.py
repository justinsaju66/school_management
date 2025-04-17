from odoo.http import request, Controller, route

class WebLeaveController(Controller):
    @route('/webform_leave', auth='public', website=True)
    def web_form(self, **kwargs):
        students = request.env['student.registration'].sudo().search([])
        print(students)
        return request.render('school_management.web_leave_template', {
            'student': students,
        })

    @route('/webform_leave/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        print('hi')
        student_id = int(post.get('student_id'))
        request.env['manage.leave'].sudo().create({
            'student_id': student_id,
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
        })
        return request.redirect('/thank-you-page')
