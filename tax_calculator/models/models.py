
from openerp import models, fields, api

class TaxCalculator(models.Model):

    _name = 'tax_calculator'
    _description = 'Tax Calculator'

    name = fields.Char('Name')
    date_from = fields.Date(string='Date From', required=True, index=True, copy=False, default=fields.Datetime.now)
    date_to = fields.Date(string='Date to', required=True, index=True, copy=False, default=fields.Datetime.now)
    total_sales_done=fields.Integer('Number of Sales', readonly=True)
    tax_amount=fields.Integer('Tax Payable', readonly=True)
    total=fields.Integer(string="Total Sales Amount", readonly=True)

    @api.model
    def create(self,vals):
        """
        Override create method to generate the name 
        field values automatically
        """
        vals['name'] = 'Sales tax from %s to %s' % (vals.get('date_from'), vals.get('date_to'))
        res = super(TaxCalculator, self).create(vals)
        return res

   
    @api.multi
    def compute_tax(self):
        '''
        This method takes self as params and compute the tax for the sales.
        '''
        total=total_sales_done=tax_amount=0.0
        
        sale_orders = self.env['sale.order'].search([('date_order', '<=', self.date_to), ('date_order', '>=', self.date_from)])
        
        for sale_order in sale_orders:
            self.total_sales_done=self.total_sales_done+1
            total=total+sale_order.amount_total
            tax_amount=tax_amount+sale_order.amount_tax
            self.total=total
            self.tax_amount=tax_amount