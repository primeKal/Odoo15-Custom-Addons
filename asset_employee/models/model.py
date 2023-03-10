from odoo import fields, models, api, registry, sql_db,_
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

class ExtendedAssetEmployee(models.Model):
    _inherit = 'account.asset'

    employee = fields.Many2one('hr.employee', string="Owner")
    reference_no = fields.Char(string='Tag Number', required=True,
                          readonly=True, default=lambda self: _('New'))
    @api.model
    def create(self, vals):
        _logger.info(vals.get('state'))
        if vals.get('reference_no', _('New')) == _('New') and not vals.get('state') == 'model':
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'account.asset') or _('New')
        res = super(ExtendedAssetEmployee, self).create(vals)
        return res



class ExtendedResPartner(models.Model):
    _inherit = 'hr.employee'


    asset_count = fields.Integer(compute='compute_count')





    def compute_count(self):
        for record in self:
            record.asset_count = self.env['account.asset'].search_count(
                [('employee', '=', self.id),('state','!=','model')])

    def get_vehicles(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assets',
            'view_mode': 'tree',
            'res_model': 'account.asset',
            'domain': [('employee', '=', self.id),('state','!=','model')],
            'context': "{'create': False}"
        }