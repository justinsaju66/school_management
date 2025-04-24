from odoo import http
from odoo.http import request, Controller, route

class WebEventController(Controller):

    @route(['/webform_event_view','/webform_event_view/page/<int:page>'], auth='public', website=True)
    def web_event_view(self,page=1, **kwargs):
        """form view and pagination for the view"""
        event_obj = request.env['manage.event']
        total_students = event_obj.search_count([])
        page_detail = request.website.pager(
            url='/webform_view',
            total=total_students,
            page=page,
            step=10,
        )
        events = event_obj.sudo().search([], offset=page_detail['offset'], limit=10)
        values = {'events': events, 'pager': page_detail}
        return request.render('school_management.event_list_template',values )

    @route('/webform_event_view/webform_event', auth='public', website=True)
    def web_event(self, **kwargs):
        """Form view for register new event through website"""
        clubs = request.env['manage.club'].sudo().search([])
        return request.render('school_management.web_event_template', {
            'club': clubs,
        })

    @route('/webform_event/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_event_submit(self, **post):
        """Method for submitting button in website"""
        club_id = int(post.get('club_id'))
        request.env['manage.event'].sudo().create({
            'name': post.get('name'),
            'club_id': club_id,
            'event_date': post.get('event_date'),
            'active': post.get('active'),
        })
        return request.render('school_management.thank_you_page')

    @http.route('/event/<model("manage.event"):event>/', auth='public', website=True)
    def student_event_list(self, event):
        """To view event details"""
        return http.request.render('school_management.student_event_details', {
            'event': event
        })
