# -*- coding: utf-8 -*-
#############################################################################
#
#    Farbell Enterprises Pvt Ltd.
#
#    Copyright (C) 2024 -TODAY Farbell Enterprises Pvt Ltd(<https://www.netconnect.co.zw>)
#    Author: Farbell Enterprises (<https://www.netconnect.co.zw>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
import re

from odoo import models, fields, api
import math

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_invoice(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        invoice_id = self.env['account.move'].search(
            [('ref', '=', pos_id.name)])
        print(invoice_id.Message)
        return {
            'invoice_id': invoice_id.id,
            'invoice_name': invoice_id.name,
            'base_url': base_url,
            'qr_code': invoice_id.QRcode,
            'verification_code' : invoice_id.VerificationCode,
            'deviceid' : invoice_id.DeviceID,
            'fiscalday': invoice_id.FiscalDay,
            'usdbp': invoice_id.partner_id.bpUsdNo,
            'zwlbp': invoice_id.partner_id.bpZwlNo,
            'zwlvat': invoice_id.partner_id.ZWLVat,
            'message': invoice_id.Message,

        }