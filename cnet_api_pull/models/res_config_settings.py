# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
from odoo import fields, models
from odoo.http import request
import requests
import dateutil.relativedelta
import logging
import json

_logger = logging.getLogger(__name__)


class ResConfigSettingsExtended(models.TransientModel):
    _inherit = ['res.config.settings']

    cnet_url = fields.Char(
        string='Cnet Url', config_parameter='cnet_api_pull.cnet_url')
    fetch_interval = fields.Char(
        string="Fetch Interval", config_parameter="cnet_api_pull.fetch_interval")
    start_date = fields.Datetime(
        string="Start", config_parameter="cnet_api_pull.start_date")
    end_date = fields.Datetime(
        string="Finish", config_parameter="cnet_api_pull.finish_date")
    specific = fields.Boolean(
        string='Specific date', default=False, config_parameter='cnet_api_pull.specific')


# END POINTS
GET_SALES = '/cnet/api/SalesOrder'
GET_EMPLOYEES = '/cnet/api/Employee'
GET_PRODUCTS = '/cnet/api/products'
GET_UNIT_OF_MEASURE = '/cnet/api/unit-of-measures'
GET_CUSTOMER = '/Cnet/api/Customer'
GET_PRODUCT_CATEG = '/cnet/api/product-categories'

# GET singles

GET_A_PRODUCT = '/cnet/api/product/code'
GET_A_CUSTOMER = '/Cnet/api/Customer/code'
GET_AN_EMPLOYEE = '/Cnet/api/Employee/code'

DEFAULT_CUSTOMER = 1


class ExtendSaleFor(models.Model):
    _inherit = 'sale.order'
    cashier = fields.Many2one('hr.employee', string="Cashier")
    is_credit = fields.Char(string='Sales Type')
    payment_method = fields.Char('Payment Method')

    def fetch_sales(self):
        specific = self.env['ir.config_parameter'].get_param(
            "cnet_api_pull.specific")
        BASE_url = self.env['ir.config_parameter'].get_param(
            "cnet_api_pull.cnet_url")
        sale_env = self.env['sale.order']
        if specific:
            endTime = self.env['ir.config_parameter'].get_param(
                "cnet_api_pull.finish_date")
            startTime = self.env['ir.config_parameter'].get_param(
                "cnet_api_pull.start_date")
        else:
            endTime = datetime.datetime.now()
            startTime = endTime + \
                dateutil.relativedelta.relativedelta(days=-15)
            endTime = endTime.strftime("%Y-%m-%d %H:%M:%S")
            startTime = startTime.strftime("%Y-%m-%d %H:%M:%S")
        data = {"startDate": startTime, "endDate": endTime}
        header = {
            "Content-Type": "application/json", }
        response = requests.get(BASE_url + GET_SALES,
                                json=data, headers=header)
        data_array = response.json()
        for sale in data_array:
            self.env.cr.commit()
            _logger.info(sale)
            sale_data = sale_env.search([('name', '=', sale['voucherCode'])])
            if not sale_data:
                # the sale order is new so lets create it
                pay = sale['voucherDefinitiona']
                if pay == 106:
                    credit = 'Cash'
                elif pay == 108:
                    credit = 'Credit'
                elif pay == 167:
                    credit = 'Manual Cash'
                elif pay == 168:
                    credit = 'Manual Credit'
                else:
                    credit = 'null'
                # match pay:
                #     case 106:
                #         credit = 'Cash'
                #     case 108:
                #         credit = 'Credit'
                #     case 167:
                #         credit = 'Manual Cash'
                #     case 168:
                #         credit = 'Manual Credit'
                #     case _:
                #         credit = 'Null'

                new_sale = sale_env.create({
                    'name': sale['voucherCode'],
                    'partner_id': self.find_or_create_customer(sale['customer']).id,
                    'cashier': self.find_or_create_employee(sale['cashier']).id,
                    'date_order': sale['quotation'].replace('T', ' ').split('.')[0],
                    'is_credit': credit,
                    'payment_method': sale['paymentMethod']
                })
                for product in sale['products']:
                    prod_id = self.find_or_create_product(
                        product['productCode'], product['unitPrice'])
                    val = {
                        "product_id": prod_id.id,
                        "order_id": new_sale.id,
                        'name': prod_id.name,
                        'price_unit': prod_id.list_price,
                        'product_uom_qty': product['quantity'],
                        'customer_lead': 30,
                        'company_id': self.company_id.id,
                    }
                    if not product['discount'] == None:
                        val['discount'] = product['discount']

                    order_line_object = self.env['sale.order.line'].create(val)
                    new_sale.write({'order_line': [(4, order_line_object.id)]})
                    order_line_object._onchange_discount()

    def find_or_create_customer(self, vals):
        _logger.info(vals)
        if vals == 'null':
            return self.env['res.partner'].search([('id', '=', DEFAULT_CUSTOMER)])
        customer = self.env['res.partner'].search(
            [('cnet_code', '=', str(vals))])
        _logger.info(customer)
        if not customer:
            BASE_url = self.env['ir.config_parameter'].get_param(
                "cnet_api_pull.cnet_url") + GET_A_CUSTOMER
            response = requests.get(BASE_url, params={'code': vals})
            _logger.info(response.content)
            if response.content == b'':
                customer = self.env['res.partner'].create({
                    'display_name': vals,
                    'name': vals,
                    'cnet_code': vals,
                })
                return customer

            res_data = response.json()
            customer = self.env['res.partner'].create({
                'display_name': res_data['name'],
                'name': res_data['name'],
                'cnet_code': res_data['code'],
                'vat': res_data['tin']
            })
        return customer

    def find_or_create_product(self, vals, price):
        product = self.env['product.product'].search([('barcode', '=', vals)])
        if not product:
            BASE_url = self.env['ir.config_parameter'].get_param(
                "cnet_api_pull.cnet_url") + GET_A_PRODUCT
            # here we will fetch the product by its code
            response = requests.get(BASE_url, params={'code': vals})
            res_data = response.json()
            _logger.info(res_data)
            product = self.env['product.product'].create({
                'name': res_data['productName'],
                # 'price': res_data[''],
                'categ_id': self.find_or_create_category(res_data['productCategory']).id,
                'list_price': price,
                'barcode': vals,
                'uom_id': self.find_or_create_uom(res_data['unitOfMeasure']).id,
                'uom_po_id': self.find_or_create_uom(res_data['unitOfMeasure']).id
            })
        return product

    def find_or_create_employee(self, vals):
        employee = self.env['hr.employee'].search([('cnet_code', '=', vals)])
        if not employee:
            BASE_url = self.env['ir.config_parameter'].get_param(
                "cnet_api_pull.cnet_url") + GET_AN_EMPLOYEE
            response = requests.get(BASE_url, params={'code': vals})
            if response.content == b'':
                employee = self.env['hr.employee'].create({
                    'display_name': vals,
                    'name': vals,
                    'cnet_code': vals,
                })
                return employee
            res_data = response.json()
            _logger.info(res_data)
            employee = self.env['hr.employee'].create({
                'name': res_data['name'],
                'cnet_code': res_data['code'],
            })
        return employee

    def find_or_create_category(self, vals):
        _logger.info('serching categ with')
        _logger.info(vals)
        categ = self.env['odoo.cnet'].search([('cnet_name', '=', vals)])
        if not categ:
            categ = self.env['product.category'].search([('id', '=', 1)])
        else:
            categ = categ[0].odoo_categ
        return categ

    def find_or_create_uom(self, vals):
        _logger.info('serching uom with')
        _logger.info(vals)
        uom = self.env['uom.uom'].search([('cnet_code', '=', vals)])
        if not uom:
            uom = self.env['uom.uom'].search([('id', '=', 1)])
        return uom

    def find_or_create(self, model, vals, search_param='name'):
        _logger.info('hiiiiiiiiiii')
        model_env = self.env[model]
        element = model_env.search([search_param, '=', vals[search_param]])
        if not element:
            element = model_env.create(vals)
        return element.id

        def confirm_sale_orders(self):
            _logger.info("YUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU1")
            date_sale = datetime.datetime(2022, 1, 6)
            mo = self.env['sale.order'].search(
                [("invoice_status", "=", "to invoice"), ("cashier", '!=', False)], order="date_order asc")

            _logger.info("YUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU2")
            count_all = 0
            count = 0

            # client = erppeek.Client('http://139.59.215.163:8055',
            #                         'Lewis_Till_Jan_30', 'admin', 'Zmall8707Odoo')
            # mo_back = client.model('mrp.production')
            sales_not_to_be_validated = [
                'CSPL3-47339-22', 'CSPL4-07772-22', 'CSPL3-47338-22']
            for m in mo:
                _logger.info(m.name)
                count_all += 1
                count += 1
                _logger.info(m.payment_method)
                _logger.info(m.cashier)
                if m.state == 'draft':
                    _logger.info(
                        "*******************Sales**************************1")
                    try:
                        m.action_confirm()
                    except:
                        pass
                    _logger.info(
                        "*******************Sales**************************")
                    _logger.info(count_all)
                    if count > 5:
                        count = 0
                        self.env.cr.commit()

        def action_confirm(self):
            count = 1
            # imediate_obj = self.env['stock.immediate.transfer']
            res = super(SaleOrder, self).action_confirm()
            for order in self:
                order._create_invoices()

                for invoice in order.invoice_ids:
                    invoice.action_post()
                    if order.website_id == False:
                        j_id = order.cashier.x_studio_csh_account.id if order.cashier else False
                        payment_vals = {
                            'date': order.date_order,
                            'amount': invoice.amount_total,
                            'payment_type': 'inbound',
                            'partner_type': 'customer',
                            'journal_id': j_id,
                            'currency_id': 79,
                            'partner_id': invoice.partner_id.id,
                            'partner_bank_id': False,
                            'payment_method_id': 1,
                            # 'destination_account_id':invoice.line_ids[0].account_id.id
                        }
                        pay = self.env['account.payment'].create(payment_vals)
                        pay.action_post()
                        domain = [('account_internal_type', 'in',
                                   ('receivable', 'payable')), ('reconciled', '=', False)]
                        payment_lines = pay.line_ids.filtered_domain(domain)
                        for account in payment_lines.account_id:
                            (payment_lines + invoice.line_ids).filtered_domain(
                                [('account_id', '=', account.id), ('reconciled', '=', False)]).reconcile()
                count = count+1
                if count == 2:
                    self.env.cr.commit()
                    count = 0

            return res
