from odoo import models, fields, api
import requests
import json

class Zreport(models.Model):
    _name = 'revmax_v3.zreport'
    _description = 'Model for storing Revmax zreports Responses'
    company_info = fields.Text(company_dependent=True)
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)
    Code = fields.Integer()
    Message = fields.Text()
    QRcode = fields.Char()
    VerificationCode = fields.Char()
    VerificationLink = fields.Char()
    DeviceID = fields.Integer()
    FiscalDay = fields.Integer()
    Zreport = fields.Text()


    def open_fiscal_day(self):
        for rec in self:
            if not rec.Message:
                url = '/api/RevmaxAPI/ZReport'
                url = rec.company_id.revmaxurl + url
                try:
                    x = requests.get(url, timeout=600)
                    data = x.json()
                    rec.Code = data.get("Code")
                    rec.Message = data.get("Message")
                    rec.QRcode = data.get("QRcode")
                    rec.VerificationCode = data.get("VerificationCode")
                    rec.VerificationLink = data.get("VerificationLink")
                    rec.DeviceID = data.get("DeviceID")
                    rec.FiscalDay = data.get("FiscalDay")
                    rec.Zreport = json.dumps(data.get("Data"), indent=4, sort_keys=True)

                    text = str(json.dumps(data, indent=4, sort_keys=True))
                    print(rec.Zreport)
                    return text

                except Exception as e:
                    return json.dumps(str(e))
            else:
                break

    def get_card_details(self):
        for rec in self:
            url = '/api/RevmaxAPI/GetCardDetails'
            url = rec.company_id.revmaxurl + url
            try:
                x = requests.get(url, timeout=15)
                return x.text
            except Exception as e:
                return json.dumps(str(e))
