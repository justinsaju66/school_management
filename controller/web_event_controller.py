from odoo.http import request, Controller, route

class WebEventController(Controller):

    @route('/webform_event_view', auth='public', website=True)
    def web_form_view(self, **kwargs):
        events = request.env['manage.event'].sudo().search([])
        return request.render('school_management.event_list_template', {
            'events': events,
        })
    @route('/webform_event_view/webform_event', auth='public', website=True)
    def web_form(self, **kwargs):
        clubs = request.env['manage.club'].sudo().search([])
        print(clubs)
        return request.render('school_management.web_event_template', {
            'club': clubs,
        })

    @route('/webform_event/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_form_submit(self, **post):
        print('hi')
        club_id = int(post.get('club_id'))
        request.env['manage.event'].sudo().create({
            'name': post.get('name'),
            'club_id': club_id,
            'event_date': post.get('event_date'),
            'active': post.get('active'),
        })
        return request.redirect('/thank-you-page')
