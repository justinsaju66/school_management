from odoo import http
from odoo.http import request, route

class ClearCart(http.Controller):
    @route('/shop/clear_cart', type='http', auth="public", website=True)
    def clear_cart(self):
        order = request.website.sale_get_order()
        if order:
            for line in order.website_order_line:
                line.unlink()
        return request.redirect('/shop/cart')
