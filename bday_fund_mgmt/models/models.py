# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import Warning


class FundCollection(models.Model):
    _name = 'fund.collection'

    
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    name = fields.Char('Description', required=True)
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
        ('12', 'December')], 'Submitted for Month', required=True)
    year = fields.Selection(
        [('2015', '2015'), 
        ('2016', '2016'), 
        ('2017', '2017'), 
        ('2018', '2018'),
        ('2019', '2019'), 
        ('2020', '2020'), 
        ('2021', '2021'),
        ('2022', '2022')], 'Submitted Year', required=True)
    state = fields.Selection([
        ('draft', 'Not Paid'),
        ('paid', 'Paid'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    amount= fields.Float('Amount Received', required=True)

    receiver_id = fields.Many2one('hr.employee', string="Receiver", domain=[('is_fund_mgr','=',True)])
    payment_date = fields.Date('Payment Date')

    @api.model
    def create(self, vals):
        months = [('1', 'January'),('2', 'February'),('3', 'March'),('4', 'April'),('5', 'May'),('6', 'June'),('7', 'July'),('8', 'August'), ('9', 'September'),('10', 'October'), ('11', 'November'), ('12', 'December')]
        month_name = dict(months).get(vals.get('month'))
        vals['name'] = 'B\'day Fund for - %s - %s' % (month_name, vals.get('year'))
        res = super(FundCollection, self).create(vals)
        return res

    @api.multi
    def action_paid(self):
        if not self.receiver_id:
            raise Warning('Please select a Receiver of the fund\n Click Modify --> Select Receiver.')
        if not self.payment_date:
            raise Warning('Please select payment date of the fund\n Click Modify --> Select Payment Date.')
        
        res = self.write({'state':'paid'})
        if res:
            notify_user = self.notify_user()
            return res
        return 

    def notify_user(self):
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('bday_fund_mgmt', 'email_template_to_fund_submission')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
                
        return self.pool['mail.template'].send_mail(self.env.cr, self.env.uid, template_id, self.id, force_send=True,context=self.env.context)

        

class Employee(models.Model):
    _inherit='hr.employee'

    is_fund_mgr = fields.Boolean('Is Fund Manager', default=False)


class Users(models.Model):
    _inherit='res.users'

    @api.model
    def create(self, vals):
        # import pdb;pdb.set_trace()
        user_id = super(Users, self).create(vals)
        employee_group_id = self.env['ir.model.data'].get_object_reference('base', 'group_user')[1]
        group_obj = self.env['ir.model.data'].get_object_reference('base', 'group_user')[0]
        group_id = self.env[group_obj].browse(employee_group_id)
        
        append_group = user_id.write({'groups_id': [(6, 0, [employee_group_id])]})

        employee = self.env['hr.employee'].create({
                'name':user_id.name,
                'work_email':user_id.login,
                'user_id':user_id.id,
            })
        return user_id



class Expense(models.Model):
    _name = 'fund.expense'

    _rec_name = 'purpose'

    employee_id = fields.Many2one('hr.employee', 'For Employee')
    purpose = fields.Selection([('bday','Birthday Expense'), ('other','Other')], required=True)
    other_reason = fields.Text('Specify Other Reason')
    expense_amount = fields.Float('Expense Amount', required=True)
    spender = fields.Many2one('hr.employee','Expensed By', required=True, domain=[('is_fund_mgr','=',True)])
    payment_date = fields.Date('Payment Date', required=True)
    state = fields.Selection([
        ('draft', 'Not Expensed'),
        ('expense', 'Expensed'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    

    @api.multi
    def action_expensed(self):
        return self.write({'state':'expense'})


