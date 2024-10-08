# -*- coding: utf-8 -*-
{
    'name': "Invoice && Account Statement",

    'summary': """
        Streamline your financial management with Invoice & Account Statement! This innovative app transforms your traditional invoice layout by seamlessly integrating comprehensive account statements.
""",

    'description': """""",

    'author': "Farbell Enterprises",
    'website': "https://www.netconnect.co.zw",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','om_account_accountant'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
    'installable': True,
}
