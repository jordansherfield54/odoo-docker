from odoo import models, fields, api
import requests
import json
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO


class AccountMove(models.Model):
    _inherit = "account.move"

    Code = fields.Char(string='Code', compute='_compute_signature', store=True, copy=False)
    Message = fields.Text(copy=False)
    QRcode = fields.Char('URL', default='', copy=False)
    VerificationCode = fields.Char(copy=False)
    VerificationLink = fields.Char(compute='_compute_signature', store=True, copy=False)
    DeviceID = fields.Char(copy=False)
    FiscalDay = fields.Char(copy=False)
    Data = fields.Text(copy=False)
    qr_code = fields.Binary(compute='_generate_qr_code')
    receiptGlobalNo = fields.Char(copy=False)

    # @api.model
    # def get_signature(self, ref):
    #     signature = self.env['pos.order'].search([('pos_reference', '=', ref)]).signature
    #
    #     return {
    #         'signature': signature
    #     }

    @api.depends("name")
    def _compute_signature(self):
        global data
        for record in self:
            if record.state == 'posted' and not record.VerificationCode:
                try:
                    ItemsXml = []
                    index = 0

                    creditnote = ""
                    # Istatus = 1 for invoice 2 for credit note
                    Istatus = ""
                    InvoiceComment = ""
                    if record.move_type == 'out_invoice':
                        Istatus = '01'
                        InvoiceComment = 'Invoice'
                    if record.move_type == 'out_refund':
                        # if move type is credit revmax needs all figures to be negative so insert - in front of all numbers
                        creditnote = "-"
                        Istatus = '02'
                        InvoiceComment = record.reversed_entry_id.name

                    if Istatus == "":
                        record.Code = ""
                        break

                    for line in record.invoice_line_ids:
                        index += 1
                        Items = {"HH": str(index),
                                 "ITEMNAME1": str(line.product_id.name),
                                 "ITEMNAME2": str(line.product_id.name),
                                 "ITEMCODE": str(line.product_id.default_code),
                                 "QTY": str(line.quantity),
                                 "PRICE": creditnote + str(round(line.price_unit, 2)),
                                 "AMT": creditnote + str(round(line.price_total, 2)),
                                 "TAX": creditnote + str(round((line.price_total - line.price_subtotal), 2)),
                                 "TAXR": str(line.tax_ids.amount / 100)}

                        ItemsXml.append(Items)

                    CurrenciesXml = [{"Name": str(record.currency_id.name),
                                      "Amount": creditnote + str(round(record.amount_total, 2)),
                                      "Rate": str(1)
                                      }]
                    result = []

                    if record.partner_id.name == "Cash Sale":
                        CustomerName = ""
                    else:
                        CustomerName = record.partner_id.name

                    if record.partner_id.vat:
                        CustomerVatNumber = record.partner_id.vat
                    else:
                        CustomerVatNumber = ""
                    if record.partner_id.contact_address and record.partner_id.name != "Cash Sale":
                        CustomerAddress = record.partner_id.contact_address
                        CustomerAddress = CustomerAddress.replace("\n", ",")
                    else:
                        CustomerAddress = ""

                    if record.partner_id.phone:
                        CustomerTelephone = record.partner_id.phone
                    else:
                        CustomerTelephone = ""

                    bpnumber = ''
                    if record.partner_id.bpUsdNo:
                        bpnumber = record.partner_id.bpUsdNo
                    else:
                        bpnumber = ""


                    #  = ""CurrenciesXml)

                    # if record.move_type == 'out_refund':
                    #     Istatus = '03'
                    #     InvoiceComment = record.reversed_entry_id.name
                    # if record.move_type =

                    myobj = {
                        "Currency": str(record.currency_id.name),
                        "BranchName": "Main",
                        "InvoiceNumber": str(record.name),
                        "CustomerName": CustomerName,
                        "CustomerVatNumber": CustomerVatNumber,
                        "CustomerAddress": CustomerAddress,
                        "CustomerTelephone": CustomerTelephone,
                        "CustomerBPN": str(bpnumber),
                        "InvoiceAmount": creditnote + str(record.amount_total),
                        "InvoiceTaxAmount": creditnote + str(record.amount_tax),
                        "Istatus": Istatus,
                        "Cashier": str(record.invoice_user_id.name),
                        "InvoiceComment": InvoiceComment,
                        "ItemsXml": ItemsXml,
                        "CurrenciesXml": CurrenciesXml
                    }
                    url = record.company_id.revmaxurl
                    url = str(url) + '/api/RevmaxAPI/TransactM'
                    headers = {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    }
                    myobj = json.dumps(myobj)
                    _logger.info(myobj)

                    # Post the data to revmax
                    x = requests.post(url, headers=headers, data=myobj, timeout=120)

                    data = x.json()
                    log = json.dumps(
                        data, indent=4)
                    _logger.info(log)
                    # if x.status_code == 200:

                    # store
                    # result in the database
                    record.Message = str(data.get("Message"))
                    record.Code = int(data.get("Code"))
                    record.QRcode = data["QRcode"]
                    record.VerificationCode = data.get("VerificationCode")
                    record.VerificationLink = data.get("VerificationLink")
                    record.DeviceID = int(data.get("DeviceID"))
                    record.FiscalDay = int(data.get("FiscalDay"))
                    record.receiptGlobalNo = data.get("Data", {}).get("receipt", {}).get("receiptGlobalNo")
                    record.Data = json.dumps(data.get("Data"), indent=4, sort_keys=True)
                    # raise ValidationError(x.text)
                except Exception as e:
                    print(e)
                    # raise ValidationError(e)
                    _logger.error(e)
                    pass

    def recompute_signature(self):
        global data
        for record in self:
            if record.state == 'posted':
                try:
                    ItemsXml = []
                    index = 0

                    creditnote = ""
                    # Istatus = 1 for invoice 2 for credit note
                    Istatus = ""
                    InvoiceComment = ""
                    if record.move_type == 'out_invoice':
                        Istatus = '01'
                        InvoiceComment = 'Invoice'
                    if record.move_type == 'out_refund':
                        # if move type is credit revmax needs all figures to be negative so insert - in front of all numbers
                        creditnote = "-"
                        Istatus = '02'
                        InvoiceComment = record.reversed_entry_id.name

                    if Istatus == "":
                        record.Code = ""
                        break

                    for line in record.invoice_line_ids:
                        index += 1
                        Items = {"HH": str(index),
                                 "ITEMNAME1": str(line.product_id.name),
                                 "ITEMNAME2": str(line.product_id.name),
                                 "ITEMCODE": str(line.product_id.default_code),
                                 "QTY": str(line.quantity),
                                 "PRICE": creditnote + str(round(line.price_unit, 2)),
                                 "AMT": creditnote + str(round(line.price_total, 2)),
                                 "TAX": creditnote + str(round((line.price_total - line.price_subtotal), 2)),
                                 "TAXR": str(line.tax_ids.amount / 100)}

                        ItemsXml.append(Items)

                    CurrenciesXml = [{"Name": str(record.currency_id.name),
                                      "Amount": creditnote + str(round(record.amount_total, 2)),
                                      "Rate": str(1)
                                      }]
                    result = []

                    if record.partner_id.name == "Cash Sale":
                        CustomerName = ""
                    else:
                        CustomerName = record.partner_id.name

                    if record.partner_id.vat:
                        CustomerVatNumber = record.partner_id.vat
                    else:
                        CustomerVatNumber = ""
                    if record.partner_id.contact_address:
                        CustomerAddress = record.partner_id.contact_address
                        CustomerAddress = CustomerAddress.replace("\n", ",")
                    else:
                        CustomerAddress = ""
                    if record.partner_id.phone:
                        CustomerTelephone = record.partner_id.phone
                    else:
                        CustomerTelephone = ""

                    bpnumber = ''
                    if record.partner_id.bpUsdNo:
                        bpnumber = record.partner_id.bpUsdNo
                    else:
                        bpnumber = ""

                    #  = ""CurrenciesXml)

                    # if record.move_type == 'out_refund':
                    #     Istatus = '03'
                    #     InvoiceComment = record.reversed_entry_id.name
                    # if record.move_type =

                    myobj = {
                        "Currency": str(record.currency_id.name),
                        "BranchName": "Main",
                        "InvoiceNumber": str(record.name),
                        "CustomerName": CustomerName,
                        "CustomerVatNumber": CustomerVatNumber,
                        "CustomerAddress": CustomerAddress,
                        "CustomerTelephone": CustomerTelephone,
                        "CustomerBPN": str(bpnumber),
                        "InvoiceAmount": creditnote + str(record.amount_total),
                        "InvoiceTaxAmount": creditnote + str(record.amount_tax),
                        "Istatus": Istatus,
                        "Cashier": str(record.invoice_user_id.name),
                        "InvoiceComment": InvoiceComment,
                        "ItemsXml": ItemsXml,
                        "CurrenciesXml": CurrenciesXml
                    }
                    url = record.company_id.revmaxurl
                    url = str(url) + '/api/RevmaxAPI/TransactM'
                    headers = {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    }
                    myobj = json.dumps(myobj)
                    _logger.info(myobj)

                    # Post the data to revmax
                    x = requests.post(url, headers=headers, data=myobj, timeout=90)

                    data = x.json()
                    log = json.dumps(
                        data, indent=4)
                    _logger.info(log)
                    # if x.status_code == 200:

                    # store
                    # result in the database
                    record.Message = str(data.get("Message"))
                    record.Code = int(data.get("Code"))
                    record.QRcode = data["QRcode"]
                    record.VerificationCode = data.get("VerificationCode")
                    record.VerificationLink = data.get("VerificationLink")
                    record.DeviceID = int(data.get("DeviceID"))
                    record.FiscalDay = int(data.get("FiscalDay"))
                    record.receiptGlobalNo = data.get("Data", {}).get("receipt", {}).get("receiptGlobalNo")
                    record.Data = json.dumps(data.get("Data"), indent=4, sort_keys=True)

                    # raise ValidationError(x.text)
                except Exception as e:
                    print(e)
                    _logger.error(e)
                    pass

    @api.depends("QRcode")
    def _generate_qr_code(self):
        for rec in self:
            if qrcode and base64:
                try:
                    qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                    )
                    qr.add_data(rec.QRcode)
                    qr.make(fit=True)
                    img = qr.make_image()
                    temp = BytesIO()
                    img.save(temp, format="PNG")
                    qr_image = base64.b64encode(temp.getvalue())
                    rec.update({'qr_code': qr_image})
                except Exception as e:
                    print(e)
                    _logger.error(e)
                    pass

