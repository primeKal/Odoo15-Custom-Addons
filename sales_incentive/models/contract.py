from odoo import fields, models, api, registry, sql_db
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

class ExtendedHrContract(models.Model):
    _inherit = 'hr.contract'

    sales_incentive = fields.Integer('Sales Incentive', default=0)

class ExtenedPaySlip(models.Model):
    _inherit = 'hr.payslip'

    # @api.model
    # def create(self, vals):
    #     # Here we must check if the incentive has been created for the year and month

    #     res = super(ExtenedPaySlip, self).create(vals)
    #     employe = res.employee_id
    #     contracts = self.env['hr.contract'].search([('employee_id', '=',employe.id)])
    #     _logger.info('here are the contractssss we found')
    #     _logger.info(contracts)
    #     for contract in contracts:
    #         contract.write({
    #         'sales_incentive' : 0
    #         })
    #     return res

    def action_payslip_done(self):
        res = super(ExtenedPaySlip, self).action_payslip_done()
        _logger.info('0000000hiiiiiiiiiiiiiiiiiiiiiiiiiii0000000000000000000')
        # employe = self.employee_id

        # contracts = self.env['hr.contract'].search([('employee_id', '=',employe.id)])
        _logger.info('here are the contractssss we found')

        contract = self.contract_id
        _logger.info(contract)
        contract.write({
            'sales_incentive' : 0
            })
        _logger.info(contract)

    # def compute_sheet(self):
    #     res = super(ExtenedPaySlip, self).compute_sheet()
    #     _logger.info('0000000hiiiiiiiiiiiiiiiiiiiiiiiiiii0000000000000000000')
    #     employe = self.employee_id
    #     contracts = self.env['hr.contract'].search([('employee_id', '=',employe.id)])
    #     _logger.info('here are the contractssss we found')
    #     _logger.info(contracts)
    #     for contract in contracts:
    #         contract.write({
    #         'sales_incentive' : 0
    #         })
    #     return res

    @api.onchange('state')
    def _onchange_incentive(self):
        _logger.info(self.state)
        _logger.info('hhhhhhhhhhhhhhhhhhhhhhyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
        _logger.info('hhhhhhhhhhhhhhhhhhhhhhyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
        _logger.info('hhhhhhhhhhhhhhhhhhhhhhyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
    #     if self.state == 'done':
    #         _logger.info('0000000hiiiiiiiiiiiiiiiiiiiiiiiiiii0000000000000000000')
    #         # employe = self.employee_id

    #         # contracts = self.env['hr.contract'].search([('employee_id', '=',employe.id)])
    #         _logger.info('here are the contractssss we found')
    #         contract = self.contract_id
    #         contract.write({
    #             'sales_incentive' : 0
    #             })
    #         _logger.info(contract)
            # for contract in contracts:
