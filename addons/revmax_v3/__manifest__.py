# -*- coding: utf-8 -*-
{
    'name': "Revmax V3",

    'summary': """
        Module for Fiscalizing invoices using the Revmax API""",

    'description': """
        Module for Fiscalizing invoices using the Revmax API
        
        To fiscalize an invoice first open the company settings and set the revmaxurl. 
        The revmax Web service is setup by Axis Solutions. 
        
        Then go to Revmaxv3 > zreport > New > Zreport to open the Fiscal Day. 
        Incoices can then be created as normal and will be sent to Zimra. 
        A Zreport needs to be Generated at day end.
    """,

    'author': "Farbell Enterprises",
    'website': "https://www.netconnect.co.zw",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '1.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sale_order.xml',
        'views/invoice_view.xml',
        'views/report_invoice_document_qrcode.xml',
        'views/report_invoice_document_tax.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'security/multi_Company_security.xml',
        'report/zreport.xml',
        'report/zreport_template.xml'

    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    # 'assets': {
    #     'web.assets_backend': [
    #         '/revmax_v3/static/src/js/sale_tree_extend.js',
    #         '/revmax_v3/static/src/xml/sale_list_button.xml',
    #
    #     ]
    # },
}
