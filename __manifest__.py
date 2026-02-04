# -*- coding: utf-8 -*-
{
    'name': "Ambassador Coupons",
    'summary': "Provide discount coupon usage information to brand ambassadors",
    'description': """
Odoo module for brand ambassadors to track their discount coupon usage.
===================================

This module allows:
- Assigning "Ambassador" status to portal users
- Linking ambassadors to one or more discount codes
- Displaying graphs of code usage (total and validated orders)
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Sales/Point of Sale',
    'version': '18.0.1.0.0',
    'depends': ['base', 'sale', 'website', 'website_sale', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'security/ambassador_security.xml',
        'views/ambassador_views.xml',
        'views/templates.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
