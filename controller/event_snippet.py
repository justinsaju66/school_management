from odoo import http


class EventSnippet(http.Controller):
    @http.route(['/school_event_snippet'], type="json", auth="public", website=True, methods=['POST'])
    def all_courses(self):
        event = http.request.env['manage.event'].search_read(
            [('website_published', '=', True)], ['name', 'image_1920', 'id'],
            order='create_date desc', limit=10)
        return event
