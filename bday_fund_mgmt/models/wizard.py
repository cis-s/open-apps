# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import Warning

class GenerateDuesWizard(models.TransientModel):
    
    _name = 'generate.dues.wizard'

    month = fields.Selection(
        [('1', 'January'), 
        ('2', 'February'), 
        ('3', 'March'), 
        ('4', 'April'),
        ('5', 'May'), 
        ('6', 'June'), 
        ('7', 'July'),
        ('8', 'August'), 
        ('9', 'September'),
        ('10', 'October'), 
        ('11', 'November'), 
        ('12', 'December')], 'Month', required=True)
    
    year = fields.Selection(
        [('2015', '2015'), 
        ('2016', '2016'), 
        ('2017', '2017'), 
        ('2018', '2018'),
        ('2019', '2019'), 
        ('2020', '2020'), 
        ('2021', '2021'),
        ('2022', '2022')], 'Year', required=True)

    amount= fields.Float('Amount', required=True)

    @api.multi
    def generate_dues(self):

        if self.amount == 0:
            raise Warning('Amount Cannot be Zero.')

        employee_ids = self.env['hr.employee'].search([])

        for employee in employee_ids:
            vals = {'employee_id':employee.id, 'month': self.month , 'year': self.year, 'state':'draft', 'amount':self.amount}
            res = self.env['fund.collection'].create(vals)

        return 

