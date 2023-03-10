from odoo import fields, models, api, registry, sql_db,_
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)



class CnetOdooMap(models.Model):
    _name = "odoo.cnet"
    _description = "This is to map cnet woth odoo categories"
    
    
    
    cnet_name = fields.Char('CNET Name', required= True)
    odoo_categ = fields.Many2one('product.category', string="Odoo")


class ExtendedHrEmployee(models.Model):
    _inherit = 'hr.employee'


    cnet_code = fields.Char(string='CNET Code')
    
class ExtendedCustomer(models.Model):
    _inherit = 'res.partner'


    cnet_code = fields.Char(string='CNET Code')

    
class ExtendedUomUom(models.Model):
    _inherit = 'uom.uom'
    
    
    cnet_code = fields.Char(string='CNET Code')
    
