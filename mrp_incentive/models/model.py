from odoo import fields, models, api, registry, sql_db
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

class ExtendedHrContract(models.Model):
    _inherit = 'hr.contract'

    mrp_incentive = fields.Integer('Mrp Incentive', default=0)
class EmployeeTOType(models.Model):
    _name = 'mrp.incentive.type'

    employ_ids = fields.Many2one('hr.employee',string="Employee")
    role = fields.Selection([
        ('Superviser','superviser'),
        ('Assistant','assistant')
    ],string='Employee Role', default= 'assistant')

class ExtendedMrpWorkCenterrrr(models.Model):
    _inherit = 'mrp.workcenter'

    # employ_ids = fields.Many2many('hr.employee',string="Memeber(Employee)")
    employee_types = fields.Many2many('mrp.incentive.type', string="Employees")
    target = fields.Float('Target')

class MrpIncentive(models.Model):
    _name = 'mrp.incentive'

    name = fields.Char(string='Name')
    state = fields.Selection([
        ('Draft','Draft'),
        ('Approved','Approved')
    ],string='Status', default= 'Draft')
    work_operation = fields.Many2one('mrp.workcenter', string="Manufacturing Operation",required=True)

    percent = fields.Integer(string="Percentage Achived", default=1, required=True)

    target = fields.Float(string="Tareget-/Month", required=True, default=1)
    paid_amount = fields.Float('Paid Amount', required=True)
    start_date = fields.Datetime(string="Start Time",required=True)
    end_date = fields.Datetime(string="End Time", required=True)
    production_count =fields.Integer('Order Count', required=True)
    production_amount =fields.Float('Total Production Qty', required=True)



    @api.onchange('work_operation','end_date','start_date')
    def _onchange_incentive(self):
        _logger.info('-------------------hiiiiiii kalupatraaaa')
        if self.start_date and self.end_date:
            production = self.env['mrp.production'].search([('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),('state','=','done')])
        else:
            production = self.env['mrp.production'].search([('state','=','done')])
        _logger.info(production)
        total = 0
        count = 0
        for mrp_pro in production:
            for  line in mrp_pro.workorder_ids:
                _logger.info(line)
                if line.workcenter_id == self.work_operation:
                    count += 1
                    _logger.info('hyyy this is the work center we found')
                    total += mrp_pro.product_qty
        self.production_amount = total
        self.target = self.work_operation.target
        self.production_count = count
        if self.target == 0:
            return
        per = total/self.target * 100
        self.percent  = per
        to_pay = '_50'
        pay = 0
        if per> 100:
            _logger.info('founddddddddddd')
            _logger.info('100')
            to_pay = '_100'
        elif per> 90:
            _logger.info('founddddddddddd')
            _logger.info('90')
            to_pay = '_90'
        elif per > 80:
            _logger.info('founddddddddddd')
            _logger.info('80')
            to_pay= '_80'
        elif per > 65:
            _logger.info('founddddddddddd')
            _logger.info('65')
            to_pay= '_65'
        else:
            to_pay = '_50'
        _logger.info('-----------------------fetching the param config for---------------')
        _logger.info(to_pay)
        _logger.info('here are the list of price ruless')
        param = 'mrp_incentive.' + to_pay
        _logger.info(param)
        _logger.info(self.env['ir.config_parameter'].get_param(param))
        pay = self.env['ir.config_parameter'].get_param(param)
        self.paid_amount = pay
        

    def giveIncentive(self):
        print('sdfksdjflksdjflksm,xcvxcm,vnrtiogrehgh[q934ero')
        employees = self.work_operation.employee_types
        for employe in employees:
            contract = self.env['hr.contract'].search([('employee_id', '=',employe.employ_ids.id)])
            _logger.info('here are the contractssss we found')
            _logger.info(contract)
            contract.write({
                'mrp_incentive' : self.paid_amount
            })
class ExtenedPaySlip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        res = super(ExtenedPaySlip, self).action_payslip_done()
        _logger.info('0000000hiiiiiiiiiiiiiiiiiiiiiiiiiii0000000000000000000')
        # employe = self.employee_id

        # contracts = self.env['hr.contract'].search([('employee_id', '=',employe.id)])
        _logger.info('here are the contractssss we found')

        contract = self.contract_id
        _logger.info(contract)
        contract.write({
            'mrp_incentive' : 0
            })
        _logger.info(contract)