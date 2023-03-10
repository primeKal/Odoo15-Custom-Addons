from odoo.exceptions import ValidationError
from odoo import api, fields, models
from odoo.http import request

from odoo.exceptions import UserError

import json
from werkzeug import urls
import pprint

import logging

_logger = logging.getLogger(__name__)


class PaymentAcquirerThawani(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[
        ('zemen', 'zemen')
    ], default='zemen', ondelete={'zemen': 'set default'})

    zemen_app_id = fields.Char(string= 'Zemen Bank AppId',
                                   required_if_provider='zemen',
                                   groups='base.group_user')



    @api.model
    def _get_zemen_urls(self):
        """ Atom URLS """
        return {
            'zemen_form_url': '/begin2'
        }

    def zemen_get_form_action_url(self):
        return self._get_zemen_urls()['zemen_form_url']

    def zemen_form_generate_values(self, values):
        _logger.info(
            'ZEMEN : preparing all form values to send to ZEMEN form url')
        # product_list = self.get_products(values['reference'])
        request_string = self.validate_data(values)
        request_string['zemen_app_id'] = self.zemen_app_id

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        request_string.update({

            # 'products': product_list,
            'return_url': urls.url_join(base_url, '/returnUrl')
        })
        return request_string

    @api.model
    def _get_compatible_acquirers(self, *args, is_validation=False, **kwargs):
        """ Override of payment to unlist Ogone acquirers for validation operations. """
        _logger.info('ZEMEN : fuckkkkkkkkkk')

        acquirers = super()._get_compatible_acquirers(*args, is_validation=is_validation, **kwargs)

        if is_validation:
            acquirers = acquirers.filtered(lambda a: a.provider != 'zemen')

        return acquirers
    def _get_default_payment_method_id(self):
        _logger.info('ZEMEN : fuckkkkkkkkkk11111111')
        self.ensure_one()
        if self.provider != 'mollie':
            return super()._get_default_payment_method_id()
        return self.env.ref('zemen_payment_acquirer.payment_method_zemen').id

    # def get_products(self, reference):
    #     txs = self.env['payment.transaction'].search([('reference', '=', reference)])
    #     txs[0].currency_id = self.company_id.currency_id
    #     sale_order = txs[0].sale_order_ids
    #     if sale_order:
    #         products = sale_order[0].website_order_line
    #         if not products:
    #             raise UserError('Please Add Products')
    #     else:
    #         invoice_orders = txs[0].invoice_ids
    #         invoice_line = invoice_orders.invoice_line_ids
    #         products = invoice_line.product_id
    #     product_list = []
    #     x = 0
    #     for product in products:
    #         print(product.name)
    #         try:
    #             quantity = product.product_uom_qty
    #         except:
    #             quantity = invoice_line[x].quantity
    #         product_list.append({"name": product.name,
    #                              "quantity": quantity})
    #         x = x + 1
    #     product_list = json.dumps(product_list)
    #     print(product_list)
    #     return product_list

    def validate_data(self, values):
        _logger.info(
            'ZEMEN: Validating all form data')
        if  not values['partner_phone'] \
                or values['amount'] == 0 \
                or not values['reference']:
            raise UserError(
                'Please Insert all available information about customer' + 'phone \n  '
                                                                           ' amount')

        request_string = {
            "phone": values['partner_phone'],
            "app_order_id": values['reference'],
            "totalAmount": values['amount'],
            # "zemen_app_id": values['zemen_app_id'],
        }

        return request_string


class PaymentTransactionZemen(models.Model):
    _inherit = 'payment.transaction'

    zemen_txn_type = fields.Char('Transaction type')

    @api.model
    def _zemen_form_get_tx_from_data(self, data):
        if data.get('tx_ref') :
            tx_ref = data.get('tx_ref')
        else :
            tx_ref = data.get('data').get('tx_ref')
        txs = self.search([('reference', '=', tx_ref)])
        return txs

    def _zemen_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        return invalid_parameters

    def _zemen_form_validate(self, data):
        _logger.info(
            'ZEMEN: Validate transaction pending or done')
        # tx_ref = data.get('tx_ref')
        # res = {
        #     'acquirer_reference': tx_ref,
        #     'zemen_txn_type': 'Zemen Payment'
        # }
        # self._set_transaction_done()
        # self.write(res)
        # _logger.info(
        #     'ZEMEN: Done when called transaction done from notify URL')
        # return True

        # if data.get('status') == 'success' :
        #     tx_ref = data.get('data').get('tx_ref')
        #     res = {
        #         'acquirer_reference': tx_ref,
        #         'zemen_txn_type':'Zemen Payment'
        #     }
        #     self._set_transaction_done()
        #     self.write(res)
        #     _logger.info(
        #         'ZEMEN: Done when called transaction done from notify URL')
        #     return True
        # else:
        #     self._set_transaction_pending()
        #     return True



    def _get_specific_create_values(self, provider, values):
        """ Complete the values of the `create` method with acquirer-specific values.

        For an acquirer to add its own create values, it must overwrite this method and return a
        dict of values. Acquirer-specific values take precedence over those of the dict of generic
        create values.

        :param str provider: The provider of the acquirer that handled the transaction
        :param dict values: The original create values
        :return: The dict of acquirer-specific create values
        :rtype: dict
        """
        print(provider)
        print(values)
        _logger.info('-------------------------------------------------------------------------------------------------------')
        _logger.info(values)
        rendering_values = {
            # "amount": self.amount,
            # "phone": '',
            # "description": '',
            # "code": "0005",
            # 'reference': '',
            # 'trace_no': 'order_id',
            # # 'trace_no': '150381222_150380222',
            # 'appId': self.acquirer_id.zemen_app_id,
            # 'api_url': 'http://localhost:8069/returnUrl2',
            'zemen_txn_type':'True'
        }

        return rendering_values

    def _get_specific_processing_values(self, processing_values):
        """ Override of payment to return Adyen-specific processing values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic processing values of the transaction
        :return: The dict of acquirer-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_processing_values(processing_values)
        if self.provider != 'zemen':
            return res
        _logger.info('--------------2-------------2-----------2----------------------------')
        _logger.info(processing_values)
        processing_values['api_url'] = 'http://localhost:8069/returnUrl2'
        return processing_values
    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Alipay-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of acquirer-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        _logger.info('please work or start something')
        if self.provider != 'zemen':
            return res

        base_url = self.acquirer_id.get_base_url()
        if self.fees:
            # Similarly to what is done in `payment::payment.transaction.create`, we need to round
            # the sum of the amount and of the fees to avoid inconsistent string representations.
            # E.g., str(1111.11 + 7.09) == '1118.1999999999998'
            total_fee = self.currency_id.round(self.amount + self.fees)
        else:
            total_fee = self.amount
        rendering_values = {
            "amount": self.amount,
            "phone": '',
            "description": '',
            "code": "0005",
            # 'reference': post['app_order_id'],
            # 'trace_no': order_id,
            # 'trace_no': '150381222_150380222',
            'appId': self.acquirer_id.zemen_app_id,
            'api_url': 'http://localhost:8069/returnUrl2',
        }

        return rendering_values
    def _send_payment_request(self):
        """ Override of payment to send a payment request to Ogone.

        Note: self.ensure_one()

        :return: None
        :raise: UserError if the transaction is not linked to a token
        """
        _logger.info('please work or start something22222222222222222222222444444444444444444444444444444444444444444444444444444444444444444444444444')
        super()._send_payment_request()
        if self.provider != 'zemen':
            return
        _logger.info('please work or start something')
