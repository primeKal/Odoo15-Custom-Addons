from odoo import fields, models, api, registry, sql_db,_
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

class SalesIncentiveMonth(models.Model):
    _name = "sale.month"
    _description = "Is used to store the sales incentive of the previous month"

    name = fields.Char(string='Name')

    start_date = fields.Datetime(string="Start Time")
    end_date = fields.Datetime(string="End Time")
    goal = fields.Float(string="Target")
    paid_amount = fields.Float('Paid Amount')
    # branch = fields.Many2one('crm.team',string ='Branch/Sales Team')

# class SalesINcentivePrice(models.Model):
#     _name = "sale.incentive.price"
#     _description = "Is used to store the sales incentive of the previous month"

#     name = fields.Char(string='Name')

#     month = fields.Selection([
#         ('100', '100'),
#         ('90', '90'),
#         ('80', '80'),
#         ('65', '66'),
#         ('50','50'),
#         ('0','0')
#     ], 'Percentage', default='60')
#     pay_amount = fields.Float('Pay Amount')
    # branch = fields.Many2one('crm.team',string ='Branch/Sales Team')




class ExtendedSalesTeam(models.Model):
    _inherit = 'crm.team'

    previous_ids = fields.Many2many("sale.month",'branch', string="Previous Targets")
    # price_ids = fields.Many2many("sale.incentive.price", string="Rules")
    employee_pay_ids = fields.Many2many('hr.employee')



class SalesIncentive(models.Model):
    _name = "sale.incentive"
    _description = "Is used to store the sales incentive of the previous month"

    name = fields.Char(string='Name')
    state = fields.Selection([
        ('Draft','Draft'),
        ('Approved','Approved')
    ],string='Status', default= 'Draft')
    branch = fields.Many2one('crm.team', string="Sales/Branch Team", required=True)

    percent = fields.Integer(string="Percentage Achived", default=1, required=True)

    target = fields.Float(string="Tareget-/Month", required=True)
    paid_amount = fields.Float('Paid Amount', required=True)
    start_date = fields.Datetime(string="Start Time", required=True)
    end_date = fields.Datetime(string="End Time", required=True)
    sales_count =fields.Integer('Sales Count', required=True)
    sales_amount =fields.Float('Total Sales', required=True)


    @api.onchange('branch','end_date','start_date')
    def _onchange_incentive(self):
        _logger.info('-------------------hiiiiiii kalupatraaaa')
        if self.start_date and self.end_date:
            sales = self.env['sale.order'].search([('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),('team_id','=',self.branch.id)])
        else:
            sales = self.env['sale.order'].search([('team_id','=',self.branch.id)])
        _logger.info(sales)
        total = 0
        import json
        for sale in sales:
            _logger.info(sale.name)
            _logger.info(sale.tax_totals_json)
            total_data = json.loads(sale.tax_totals_json)
            _logger.info(total_data)
            _logger.info(total_data['amount_total'])
            total+=int(total_data['amount_total'])
        _logger.info(self.branch.invoiced_target)
        _logger.info(total)
        invoice_target = self.branch.invoiced_target
        if invoice_target == 0 : return
        percent = (total/invoice_target) * 100
        self.percent  = percent
        self.sales_amount = total
        self.target = self.branch.invoiced_target
        _logger.info(type(sales))
        self.sales_count = len(sales)
        to_pay = 's_10'
        pay = 0
        if percent> 100:
            _logger.info('founddddddddddd')
            _logger.info('100')
            to_pay = 's_100'
        elif percent> 90:
            _logger.info('founddddddddddd')
            _logger.info('90')
            to_pay = 's_90'
        elif percent > 75:
            _logger.info('founddddddddddd')
            _logger.info('80')
            to_pay= 's_75'
        elif percent > 50:
            _logger.info('founddddddddddd')
            _logger.info('65')
            to_pay= 's_50'
        elif percent > 25:
            to_pay = 's_25'
        else:
            to_pay = 's_10'
        _logger.info('-----------------------fetching the param config for---------------')
        _logger.info(to_pay)
        _logger.info('here are the list of price ruless')
        param = 'sales_incentive.' + to_pay
        _logger.info(param)
        _logger.info(self.env['ir.config_parameter'].get_param(param))
        pay = self.env['ir.config_parameter'].get_param(param)
        self.paid_amount = pay
        # for price in price_rules:
        #     _logger.info(price.month)
        #     _logger.info(to_pay)
        #     if str(price.month) == str(to_pay):
        #         _logger.info('founddddd')
        #         pay = price.pay_amount
        #         self.paid_amount = pay
        #         return
        
    def giveIncentive(self):
        _logger.info('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        _logger.info('lets firat check the current time is not in previous targets ')
        previous_targets = self.branch.previous_ids
        from datetime import datetime
        now = datetime.now()
        if not (len(previous_targets)== 0):
            for targt in previous_targets:
                _logger.info('In the for loop of previous targets')
                if targt.start_date< now < targt.end_date:
                    _logger.info('Caution This is to indicate that the current time was found to be between previous targets')
                    raise UserError('Error Cant add Incentive to employees because they have already been paid for this month or the current time was founnd in previous targets')
        members = self.branch.employee_pay_ids
        user_employee = []
        if not (len(self.branch.member_ids)== 0 ):
            for x in self.branch.member_ids:
                user_employee.append(x.employee_id)
        if len(members) == 0 or len(user_employee) == 0:
            self.state = 'Draft'
            raise UserError('No Employees,The selected Branch has no employees, please configure')
        for employe in members:
            contract = self.env['hr.contract'].search([('employee_id', '=',employe.id)])
            _logger.info('here are the contractssss we found')
            _logger.info(contract)
            contract.write({
                'sales_incentive' : self.paid_amount
            })
        if not len(user_employee) == 0:
            for employe in user_employee:
                contract = self.env['hr.contract'].search([('employee_id', '=',employe.id)])
                _logger.info('here are the contractssss we found')
                _logger.info(contract)
                contract.write({
                    'sales_incentive' : self.paid_amount
                })
        sales_month = self.env['sale.month']
        _logger.info('-------------------------------------------hiiiii----------------------------------')
        sales_month_data = sales_month.create({
            'start_date': self.start_date,
            'end_date' : self.end_date,
            'name' : self.name,
            'goal' : self.target,
            'paid_amount': self.paid_amount
        })
        _logger.info(sales_month_data)
        branch = self.branch
        branch.write({
                        'previous_ids': [(4, sales_month_data.id)],
                        # 'attribute_id' : attribute[0].id
                    })
        _logger.info(type(branch.previous_ids))
        self.state = 'Approved'
    def findAndGiveThesePeopleThereMoney(self):
        print('getting ready to add incentive to all the memebers')
    @api.model
    def create(self, vals):
        # Here we must check if the incentive has been created for the year and month
        res = super(SalesIncentive, self).create(vals)
        return res
    # def return_notification(self, title,message,type):
    #     _logger.info('----------------------------------------------------------dsddsdsdsddssd')
    #     _logger.info(title)
    #     notification = {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': _(title),
    #             'message': message,
    #             'type':type,  #types: success,warning,danger,info
    #             'sticky': True,  #True/False will display for few seconds if false
    #         },
    #     }
    #     return notification