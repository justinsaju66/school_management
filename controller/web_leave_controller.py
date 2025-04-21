from odoo import http
from odoo.http import request, Controller, route


class WebLeaveController(Controller):

    @route(['/webform_leave_view','/webform_leave_view/page/<int:page>'], auth='public', website=True)
    def web_form_view(self,page=1, **kwargs):
        leave_obj = request.env['manage.leave']
        total_leaves = leave_obj.search_count([])
        page_detail = request.website.pager(
            url='/webform_leave_view',
            total=total_leaves,
            page=page,
            step=10,
        )
        leaves = leave_obj.sudo().search([], offset=page_detail['offset'], limit=10)
        values = {'leaves': leaves, 'pager': page_detail}
        return request.render('school_management.leave_list_template', values)

    @route('/webform_leave_view/webform_leave', auth='public', website=True)
    def web_form(self, **kwargs):
        students = request.env['student.registration'].sudo().search([])
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
            'reason': post.get('reason'),
        })
        return request.render('school_management.thank_you_page')


