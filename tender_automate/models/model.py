from odoo import fields, models, api, registry, sql_db,_
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

class ExtendedHrContract(models.Model):
    _inherit = 'purchase.requisition'

    def analyze(self):
        print('sdkjsdjkfhsdjkf')
        _logger.info('about to find these shits')
        # tender_products = self.line_ids
        tender_rfq = self.env['purchase.order'].search([('requisition_id','=',self.id)])
        _logger.info(tender_rfq)
        tenderr_object = self.env['purchase.tenderr']
        if len(tender_rfq) == 0 :
            _logger.info('thank god No rfq detected /or we can raise an error')
        # # for each tender lets find the minumemu price
        _logger.info('have started loopingggg')
        for quotation in tender_rfq:
            for order_line in quotation.order_line:
                already = tenderr_object.search([('line','=',order_line.id),('tender','=',self.id)])
                if already:
                    break
                vals = {
                    'line': order_line.id,
                    'qty' : order_line.product_qty,
                    'tender': quotation.requisition_id.id,
                    'company': quotation.partner_id.id,
                    'unit_price': order_line.price_unit,
                    'name': order_line.product_id.name
                }
                _logger.info(vals)
                tenderr_object.create(vals)

        view_id_form = self.env['ir.ui.view'].search([('name', '=', 'Analyze Tenders')])
        view = view_id_form[0]
        view = view.id
        _logger.info(view)
        _logger.info('---------------------this is the title')
        title = _(self.name)
        _logger.info(title)
        _logger.info(self)
        # return self.give_dic_act_wind('Analyze Tenders','','purchase.tenderr','For tender')
        # return a tree view
        self.action_open()
        return {'type': 'ir.actions.act_window',
            'view_type': 'form', 
            'view_mode': 'tree', 
            'res_model': 'purchase.tenderr',
            'view_id': view,
            'target': 'new',
            'domain': [('tender', '=', self.id)],
            'name': title}
    def create_selected(self):
        _logger.info('creating the purchase requirement')
        _logger.info('first lets get the purchase orders')
        purchase = self.env['purchase.order'].search([('requisition_id','=',self.id)])
        _logger.info('this is the purcase')
        _logger.info(purchase)
        for x in purchase:
            x.button_cancel()
        purchase_orders = self.env['purchase.tenderr'].search([('tender','=',self.id), ('is_selected','=',True)])
        if len(purchase_orders) == 0:
            _logger.info('none found ---------------')
            return
        # lets find unique companies
        uniq_companies = []

            
        for order in purchase_orders:
            if not order.company in uniq_companies:
                uniq_companies.append(order.company)
        _logger.info('unique companies identified')
        _logger.info(uniq_companies)
        for uniq in uniq_companies:
            order_lines  = filter(lambda order: order.company == uniq, purchase_orders)

            _logger.info('filtered order linessss')
            _logger.info(order_lines)
            _logger.info(type(order_lines))
            purchase = self.env['purchase.order'].create({
                'partner_id':uniq.id,
                'requisition_id':self.id,
            })
            _logger.info('success in creating the pruchase order')
            _logger.info(purchase)
            for lin in order_lines:
                purchase.write({
                        'order_line' : [(0,0,{
                            'product_id':lin.line.product_id.id,
                            'name': lin.line.product_id.name,
                            'product_qty': lin.qty,
                            'price_unit': lin.unit_price
                        })]
                    })
            purchase.button_confirm()
        self.action_done()
            



    def findCheapest(self, product_id,rfqs):
        _logger.info('starting to find the cheapest product')
        _logger.info(product_id)
        found = 0
        prod = None
        rfq_product = None
        for rfq in rfqs:
            _logger.info(rfq)
            _logger.info('^^^^^^^ current rfq')
            for product in rfq.order_line:
                _logger.info(product)
                _logger.info('product in rfq')
                if product_id.product_id == product.product_id:
                    _logger.info('found the matchng producttt')
                    _logger.info(product_id)
                    _logger.info(product.price_unit)
                    if found == 0 or found>product.price_unit:
                        _logger.info('found the lower price toooo')
                        found = product.price_unit
                        prod = product
                        rfq_product = rfq
        return {
            'product_line': prod,
            'rfq': rfq_product,
            'found': found
        }
    def remove_line_from_all_except_one(self, product_id,linee,rfqs):
        _logger.info('hiiiiiiiiiiiiiii')
        _logger.info('we will remove all rfqss product_id except rfq')
        for rffqqq in rfqs:
            _logger.info(rffqqq.name)
            for line in rffqqq.order_line:
                if linee == line:
                    _logger.info('skipping this')
                    break
                if product_id == line.product_id:
                    _logger.info('this is to be removed')
                    _logger.info('remove this line from the order line......')
                    rffqqq.write({
                        'order_line' : [(3,line.id)]
                    })
    def send(self):
        print('sending')
        _logger.info('hellooooooo')
        mail_pool = self.env['mail.mail']
        values={}
        values.update({'subject': 'Your subject'})
        values.update({'email_to': 'kalebteshale72@gmail.com'})
        values.update({'body_html': 'body' })
        values.update({'body': 'body' })
        # values.update({'res_id': 'obj.id' }) #[optional] here is the record id, where you want to post that email after sending
        # values.update({'model': ''Object Name }) #[optional] here is the object(like 'project.project')  to whose record id you want to post that email after sending
        msg_id = mail_pool.create(values)
        _logger.info(msg_id) 
        if msg_id:
            mail_pool.send([msg_id])

class NewPurchase(models.Model):
    _name = 'purchase.tenderr'
    _order = "name  ASC"

    line = fields.Many2one('purchase.order.line', string="Product")
    is_selected= fields.Boolean('Selected', default=False)
    tender = fields.Many2one('purchase.requisition')
    qty = fields.Integer('Quantity',default=1)
    company = fields.Many2one('res.partner')
    unit_price = fields.Float('Unit Price',default=1)
    total = fields.Float('Total',compute='totalCompute')

    name = fields.Char('Name')
 


    # @api.model
    # def create(self, vals):
    #     vals['name'] = vals['line'].name
    #     _logger.info(vals['line'].name)
    #     res = super(ExtendMrp, self).create(vals)
    #     return res




    def totalCompute(self):
        for sel in self:
            sel.total = sel.unit_price * sel.qty

    # name = fields.Char('')

    # @api.onchange('is_selected')
    # def _onchange(self):
    #     _logger.info('on change triggered----------------------------------------------------------')
    #     if self.is_selected:
    #         _logger.info('setting a row to true, lets make all false-----------------------------------------------------------')
    #         current_tender_lines = self.env['purchase.tenderr'].search([('tender','=',self.tender.id)])
    #         if current_tender_lines:
    #             for line in current_tender_lines:
    #                 if line.line.product_id == self.line.product_id:
    #                     if not (line.id == self.id):
    #                         line.is_selected=False
    #                         line.write({
    #                             'is_selected':False
    #                         })

    def select(self):
        _logger.info('on change triggered----------------------------------------------------------')
        _logger.info('setting a row to true, lets make all false-----------------------------------------------------------')
        current_tender_lines = self.env['purchase.tenderr'].search([('tender','=',self.tender.id)])
        _logger.info(current_tender_lines)
        if current_tender_lines:
            _logger.info('foundddd some tender lines')
            for line in current_tender_lines:
                if line.line.product_id == self.line.product_id:
                    _logger.info('matched the products')
                    if not (line.id == self.id):
                        # line.is_selected=False
                        _logger.info('setting False')
                        line.write({
                            'is_selected':False
                        })
                    else :
                        _logger.info('setting this one to true')
                        line.write({
                            'is_selected': True
                        })
        view_id_form = self.env['ir.ui.view'].search([('name', '=', 'Analyze Tenders')])
        view = view_id_form[0]
        view = view.id
        _logger.info(view)
        title = _(self.tender.name)
        _logger.info(title)
        # return self.give_dic_act_wind('Analyze Tenders','','purchase.tenderr','For tender')
        # return a tree view
        return {'type': 'ir.actions.act_window',
            'view_type': 'form', 
            'view_mode': 'tree', 
            'res_model': 'purchase.tenderr',
            'view_id': view,
            'target': 'new',
            'domain': [('tender', '=', self.tender.id)],
            'name': title}
 
