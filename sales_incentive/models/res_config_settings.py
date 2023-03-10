# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettingsExtended(models.TransientModel):
    _inherit = ['res.config.settings']

    s_100 = fields.Float(string='Above 100%', default=30,config_parameter='sales_incentive.s_100')
    s_90 = fields.Float(string='Above 90%', default=30, config_parameter='sales_incentive.s_90')
    s_75 = fields.Float(string='Above 75%', default=30, config_parameter='sales_incentive.s_75')
    s_50 = fields.Float(string='Above 50%', default=30, config_parameter='sales_incentive.s_50')
    s_25 = fields.Float(string='Above 25%', default=30, config_parameter='sales_incentive.s_25')
    s_10 = fields.Float(string='Above 10', default=10, config_parameter='sales_incentive.s_10')
