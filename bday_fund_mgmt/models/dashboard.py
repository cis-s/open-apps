# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields, osv
from openerp import api, fields, models, _
from datetime import datetime

class CurrentBalanceReport(models.Model):
    _name = "current.balance.report"
    _description = "Manager Balance Report"
    _auto = False
    _rec_name = 'receiver_id'


    receiver_id = fields.Many2one('hr.employee', string="Manager", domain=[('is_fund_mgr','=',True)], readonly=True)

    amount = fields.Float(string='Current Balance')        
    
    _order = 'amount asc'

    def init(self, cr):
        """
        Method to return Employee Nos.based on gender
        """
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
        	SELECT temp.id as id, temp.id as receiver_id,  (COALESCE(temp.paidamt ,0 ) - COALESCE(temp.expamt , 0) ) as amount FROM (
			SELECT he.id,
			(SELECT sum(fc.amount) as fca FROM fund_collection as fc WHERE fc.receiver_id = he.id AND fc.state='paid') as paidamt,
			(SELECT sum(fex.expense_amount) as fca FROM fund_expense as fex WHERE fex.spender = he.id AND fex.state='expense') as expamt
			FROM  hr_employee as he where he.is_fund_mgr = True) as temp
            )""" % (self._table))

