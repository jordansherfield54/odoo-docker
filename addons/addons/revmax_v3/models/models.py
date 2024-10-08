# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
headers = {
            'Content-Type': 'application/json;',
            'Accept':'application/json'
}

class revmax_v3(models.Model):
    _name = 'revmax_v3.transactm'
    _description = 'Model for storing Revmax transact Responses'

    name = fields.Char()
    Code = fields.Integer()
    Message = fields.Text()
    QRcode = fields.Char()
    VerificationCode = fields.Char()
    VerificationLink = fields.Char()
    DeviceID = fields.Integer()
    FiscalDay = fields.Integer()
    Data = fields.Text()

    def open_fiscal_day(self):
        url = 'http://localhost:8001/ZReport/ZReport'

        x = requests.get(url)

        return x.text

    def get_card_details(self):
        url = 'http://localhost:8001/card/getcarddetails'

        x = requests.get(url)
        
        return x.text





