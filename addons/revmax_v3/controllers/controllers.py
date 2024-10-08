# -*- coding: utf-8 -*-
from odoo import http


class RevmaxV3(http.Controller):
    @http.route('/revmax_v3/revmax_v3', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/revmax_v3/revmax_v3/objects', auth='public')
    def list(self, **kw):
        return http.request.render('revmax_v3.listing', {
            'root': '/revmax_v3/revmax_v3',
            'objects': http.request.env['revmax_v3.transactm'].search([]),
        })

    @http.route('/revmax_v3/revmax_v3/objects/<model("revmax_v3.transactm"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('revmax_v3.object', {
            'object': obj
        })
