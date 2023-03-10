from odoo import http
from odoo.http import request


class MyController(http.Controller):
    @http.route('/editPage', auth='public')
    def handler(self):
        # Your functions here
        values = {'name': 'Kalebbbbbb'}
        return request.render("dynamic_check_print.Check", values)
