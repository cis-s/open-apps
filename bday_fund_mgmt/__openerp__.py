# -*- coding: utf-8 -*-
{
    'name': "Fund Management System",

    'summary': """
       Fund Management System.
       """,

    'description': """
        This modules provides features of - 
       -> Fund Collection\n
       -> Fund Expenses\n
       -> Cash in hand of Managers\n
       -> Employee's Dues & Payments.\n

       Creates employee automatically on User signup.

       In Employee's Form --> HR Settings \n
       -> Check 'Is Fund Manager' checkbox to create the employee as fund manager.
    """,

    'author': "ArionERP",
    'website': "http://arionerp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/inherit_employee_view.xml',
        'views/balance_dashboard.xml',
        'views/email_template.xml',
        'views/create_due_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}