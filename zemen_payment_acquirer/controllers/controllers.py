import json
import logging
import requests
import werkzeug
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from werkzeug import urls

import pprint

_logger = logging.getLogger(__name__)


class ZemenBank(http.Controller):
    global private
    global tx_ref

    @http.route('/notifyUrl2',
                type='http', auth='public', csrf=False, methods=['GET', 'POST'], save_session=False)
    def zemenReturn(self, **post):

        request.env['payment.transaction'].sudo().form_feedback('data', 'zemen')
        return werkzeug.utils.redirect('/payment/process')

        # verify_url = "https://api.chapa.co/v1/transaction/verify/" + self.tx_ref
        # request_headers = {
        #         "Authorization": "Bearer " + str(self.private)
        # }
        # print(self.private)
        # try :
        #     res = requests.get(verify_url,headers=request_headers)
        # except Exception as e:
        #     print(e)
        #
        # _logger.info(
        #     'Chapa: entering form_feedback from retrun or notify with post data %s', pprint.pformat(post))
        if res.status_code == 200:
            data = dict(res.json())
            request.env['payment.transaction'].sudo().form_feedback(data, 'zemen')
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/returnUrl2',
                type='http', auth='public', csrf=False, methods=['POST', 'GET'], save_session=False)
    def zemenReturning(self, **post):
        post.update({
            'tx_ref': self.tx_ref
        })
        _logger.info(
            'ZEMEN: entering form_feedback from successful payment and returning(redirecting) ')
        request.env['payment.transaction'].sudo().form_feedback(post, 'zemen')
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/begin2', type='http', auth='public', csrf=False, methods=['POST'])
    def begin_transaction(self, **post):
        _logger.info(
            'ZEMEN : Begining to parse data and post to request URL')
        request_url = 'https://pgw.shekla.app/zemen/post_bill'
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.tx_ref = post['app_order_id']
        request_headers = {
            # "Authorization" : "Bearer " + post["private_key"],
            "Content-Type": "application/json",
        }
        # print(post['products'])
        # print(json.dumps(post['products']))
        # lets make a trace number following 'unique random number_ordernumber pattern'
        order_id = post['app_order_id']
        if '-' in order_id:
            temp = order_id.split('-')
            order_id = temp[0][1:]+temp[1] + '_' + str(temp[0])[1:]
        else :
            order_id = str(00) + '_' + order_id[1:]
        total =  round(float(post["totalAmount"]),3)
        # trace_number = str(post['app_order_id'][1:]) + '_' + str(post['app_order_id'][1:])
        req_data = {
            "amount": total,
            "phone": post['phone'],
            "description": post['app_order_id'],
            "code": "0005",
            'reference': post['app_order_id'],
            'trace_no': order_id,
            # 'trace_no': '150381222_150380222',
            'appId': post['zemen_app_id']
            # 'appId': '1234'

        }
        print('hereeee we are ready to send the data')
        # return werkzeug.utils.redirect('/returnUrl2')
        try:
            response = requests.post(request_url, headers=request_headers, json=req_data)
        except Exception as e:
            print(e)
        if response.status_code >= 200 and response.status_code <= 300:
            _logger.info(
                'ZEMEN : Success in post request, set transaction to pending and redirect to new Transaction Url')
            response_json = response.json()
            post.update({
                'tx_ref': post['app_order_id']
            })
            request.env['payment.transaction'].sudo().form_feedback(post, 'zemen')
            data = response_json['data']['data']
            return werkzeug.utils.redirect(response_json["data"]["data"]['toPayUrl'])
        else:
            raise werkzeug.exceptions.BadRequest(
                "Request not successful,Please check the keys or consult the admin.code-" + str(response.status_code))
            # return response.status_code
