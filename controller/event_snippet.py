from odoo import http
from odoo.http import request, route


class EventSnippet(http.Controller):
    """Snippet for Event"""

    @route('/event_snippt_templete', auth='public', website=True)
    def event_snippet_template(self, **kwargs):
        """form view of event"""
        return request.render('school_management.event_snippet_template')

    @route('/event/<model("manage.event"):event>', auth='public', website=True)
    def event_snippet(self,event, **kwargs):
        """To get all event"""
        return request.render('school_management.student_event_details',{'event': event,})

    @http.route('/get_events', auth="public", type='json',website=True)
    def get_school_event(self):
        """Get the website categories for the snippet."""
        public_categs = request.env[
            'manage.event'].sudo().search_read(fields=['name', 'id','photo'],order='create_date desc'
        )
        values = {
            'events': public_categs,
        }
        return values
