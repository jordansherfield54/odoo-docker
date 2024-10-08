# -*- coding: utf-8 -*-
# from odoo import http


# class ExtendedInvoice(http.Controller):
#     @http.route('/extended_invoice/extended_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/extended_invoice/extended_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('extended_invoice.listing', {
#             'root': '/extended_invoice/extended_invoice',
#             'objects': http.request.env['extended_invoice.extended_invoice'].search([]),
#         })

#     @http.route('/extended_invoice/extended_invoice/objects/<model("extended_invoice.extended_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('extended_invoice.object', {
#             'object': obj
#         })
