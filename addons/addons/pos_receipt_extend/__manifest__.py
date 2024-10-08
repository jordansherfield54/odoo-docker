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
{
    'name': "Advanced POS Receipt",
    "description": """Advanced POS Receipt with Customer, Invoice and fiscal Details""",
    "summary": "Advanced POS Receipt with Customer, Invoice and fiscal Details",
    "category": "Point of Sale",
    "version": "16.0.1.0.0",
    'author': 'Jordan Sherfield',
    'company': 'Farbell Enterprises',
    'maintainer': 'Jordan Sherfield',
    'website': "https://www.netconnect.co.zw",
    'depends': ['point_of_sale', 'sale', 'account', 'revmax_v3'],
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt_extend/static/src/xml/OrderReceiptSmall.xml',
            'pos_receipt_extend/static/src/js/payment.js',
            'pos_receipt_extend/static/src/js/autoprint.js',
            'pos_receipt_extend/static/src/xml/hide_print.xml',
            'pos_receipt_extend/static/src/css/reciept_font.css',
            'pos_receipt_extend/static/src/xml/hide_reprint.xml'
        ]
    },
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
