# -*- coding: utf-8 -*-
{
    'name': "Sales Tax Computation",

    'summary': """
       This module will help salesperson to compute the taxes for all the sales order""",

    'description': """
        This Module help you to compute taxes included in the sales order that will help you to compute the taxes during the sales
    """,

    'author': "CIS",
    'website': "http://www.cisin.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}