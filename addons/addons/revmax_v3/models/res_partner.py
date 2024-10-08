from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    ZWLVat = fields.Char(string="ZWL Vat Number")
    bpUsdNo = fields.Char(string="Usd Bp Number")
    bpZwlNo = fields.Char(string="Zwl Bp Number")

class ResCompany(models.Model):
    _inherit = 'res.company'
    ZWLVat = fields.Char(string="ZWL Vat Number")
    bpUsdNo = fields.Char(string="Usd Bp Number")
    bpZwlNo = fields.Char(string="Zwl Bp Number")
    revmaxurl = fields.Char(string="Revmax Device URL", help="http://localhost:100054", default='http://140.82.25.196:10002')
    # deviceID = fields.Char(string="Revmax Device ID")