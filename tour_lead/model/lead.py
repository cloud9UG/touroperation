# -*- coding: utf-7 -*_
"""
@author: Accioma
"""
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class touoperation_line(osv.Model):
    _name = 'touroperation.line'
    def _amount_acco(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for acco_line in l.acco_line_ids:
                val1 += acco_line.total_line_price
            res[l.id] = val1
        return res

    def _amount_cruise(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for cruise_line in l.cruise_line_ids:
                val1 += cruise_line.cruise_price_total
            res[l.id] = val1
        return res

    def _amount_lodge(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for lodge_line in l.lodge_line_ids:
                val1 += lodge_line.lodge_price_total
            res[l.id] = val1
        return res

    def _amount_package(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for package_line in l.package_line_ids:
                val1 += package_line.package_price_total
            res[l.id] = val1
        return res

    def _amount_transfer(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for transfer_line in l.transfer_line_ids:
                val1 += transfer_line.subtotal_line_price
            res[l.id] = val1
        return res

    def _amount_assistance(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for assistance_line in l.assistance_line_ids:
                val1 += assistance_line.subtotal_line_price
            res[l.id] = val1
        return res
    def _amount_ticket(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for ticket_line in l.ticket_line_ids:
                val1 += ticket_line.subtotal_line_price
            res[l.id] = val1
        return res
    def _amount_msc(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for l in self.browse(cr, uid, ids, context=context):
            val = val1 = 0.0
            for msc_line in l.msc_line_ids:
                val1 += msc_line.subtotal_line_price
            res[l.id] = val1
        return res
    _columns=-
            'acco_line_ids':fields.one2many('accommodation.tour.sale.orde.line',
                'tour_id','Accommodation'
                ),
            'cruise_line_ids':fields.one2many('cruise.tour.sale.orde.line',
                'tour_id','Cruise'
                ),
            'fticket_line_ids':fields.one2many('ticket.tour.sale.orde.line',
                'tour_id','Ticket'
                ),
            'lodge_line_ids':fields.one2many('lodge.tour.sale.orde.line',
                'tour_id','Lodge'
                ),
            'package_line_ids':fields.one2many('package.tour.sale.orde.line',
                'tour_id','Package'
                ),
            'transfer_line_ids':fields.one2many('transfer.tour.sale.orde.line',
                'tour_id','Transfer'
                ),
            'assistance_line_ids':fields.one2many('assistance.tour.sale.orde.line',
                'tour_id','Assistance'
                ),
            'ticket_line_ids':fields.one2many('ticket.tour.sale.orde.line',
                'tour_id','Ticket'
                ),
            'msc_line_ids':fields.one2many('misc.tour.sale.orde.line',
                'tour_id','Miscellaneous'
                ),
            'paxline_ids':fields.one2many('tour.lead.paxline', 'tour_lead_id', 'Pax'),
            'acco_amount_total':fields.function(_amount_acco,
                digits_compute=dp.get_precision('Account'),
                string='Accommodation Amount',type='float', method=True),
            'cruise_amount_total':fields.function(_amount_cruise,
                digits_compute=dp.get_precision('Account'),
                string='Cruise Amount',type='float', method=True),
            'lodge_amount_total':fields.function(_amount_lodge,
                digits_compute=dp.get_precision('Account'),
                string='Lodge Amount',type='float', method=True),
            'package_amount_total':fields.function(_amount_package,
                digits_compute=dp.get_precision('Account'),
                string='Package Amount',type='float', method=True),
            'transfer_amount_total':fields.function(_amount_transfer,
                digits_compute=dp.get_precision('Account'),
                string='Transfer Amount',type='float', method=True),
            'assistance_amount_total':fields.function(_amount_assistance,
                digits_compute=dp.get_precision('Account'),
                string='Assistance Amount',type='float', method=True),
            'ticket_amount_total':fields.function(_amount_ticket,
                digits_compute=dp.get_precision('Account'),
                string='Tticket Amount',type='float', method=True),
            'msc_amount_total':fields.function(_amount_msc,
                digits_compute=dp.get_precision('Account'),
                string='Extra Amount',type='float', method=True),
            }


    def button_dummy(self, cr, uid, ids, context=None):
        return True

class sale_order_line(osv.Model):
    """
    @description: Class intended to manage a line of sale order

    """

    def _delta_days(self, end_date, start_date):
        from datetime import datetime as DT
        dateformat = '%Y-%m-%d'
        d1 = DT.strptime(end_date, dateformat)
        d2 = DT.strptime(start_date, dateformat)
        return (d1 - d2).days

    def _fcn_nights_stay(self, cr, uid, ids, field_name, arg, context):
        result = {}
        lines = self.browse(cr, uid, ids, context)
        for l in lines:
            result[l.id] = self._delta_days(l.end_date, l.start_date)
        return result

    def _fcn_total_line_price(self, cr, uid, ids, field_name, arg, context):
        result = {}
        lines = self.browse(cr, uid, ids, context)
        for l in lines:
            nigths_stay = self._delta_days(l.end_date, l.start_date)
            result[l.id] = l.unit_price * l.qtty * nigths_stay
        return result
    def _subtotal_line_price(self, cr, uid, ids, field_name, arg, context):
        result = {}
        lines = self.browse(cr, uid, ids, context)
        for l in lines:
            result[l.id] = l.unit_price * l.qtty
        return result


    _name="tour.sale.order.line"
    _columns={
            'start_date':fields.datetime('Start date', required=True),
            'end_date':fields.datetime('End date', required=True),
            'unit_price': fields.float('Price', required=True,
                digits_compute= dp.get_precision('Product Price'),
                readonly=False ),
            'unit_cost': fields.float('Cost', required=True,
                digits_compute= dp.get_precision('Product Price'),
                readonly=False ),
            'itinerary':fields.html('Itinerary'),
            'tour_status':fields.selection(
                [
                ('option', 'Option'),
                ('block', 'Block'),
                ('confirmed', 'Confirmed'),
                ('operating', 'Operating'),
                ('closed', 'Closed'),
                ('canceled', 'Canceled'),
                ('not_operated', 'Not operated'),
                ],'Status', required=True),
            'limit_date':fields.date('Limit date', required=True),
            'qtty':fields.integer('Units', required=True),
            'acco_type':fields.char('Accommodation type', 100),
            'agent_commission':fields.integer("Agent's commission", required=True),
            'operator':fields.char('Operator', 100),
            'emergency_contact':fields.many2one('res.partner', 'Emergency \
                Contact'),
            'observations':fields.text('Observations'),
            'nigths_stay':fields.function(_fcn_nights_stay, type='integer',
                    string='Nigths Stay', method=True),
            'total_line_price':fields.function(_fcn_total_line_price, type='float',
                    string='Total Price', method=True),
            'subtotal_line_price':fields.function(_subtotal_line_price,
                method=True,
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string='Total Price',
                help='Calculated field of total price qtty*price'),

            }

    _defaults={
            'qtty':1,
            'unit_price':0.0,
            'unit_cost':0.0,
            'tour_status':'option',
            'start_date':fields.date.context_today,
            'end_date':fields.date.context_today,
            'limit_date':fields.date.context_today,

            }


    def _end_date_after_start_date(self, cr, uid, ids):
        for line in self.browse(cr, uid, ids):
            if line.start_date > line.end_date:
                return False
        return True

    def _no_date_before_today(self, cr, uid, ids):
        for line in self.browse(cr, uid, ids):
            if fields.date.context_today > line.start_date\
                    or fields.date.context_today > line.end_date\
                    or fields.date.context_today > line.limit_date:
                return False
        return True


    _constraints = [
       (_end_date_after_start_date,
        'End date after start date',
        ['start_date', 'end_date']),
       (_no_date_before_today,
        'No date shall be entered before today',
        ['start_date', 'end_date', 'limit_date']),

        ]

#Cruise
class cruise_sale_order_line(osv.Model):
    _name="cruise.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    def _price_total(self, cr, uid, ids, field, arg, context=None):
        """Calculates total price from price lines"""
        cruise_line_obj = self.browse(cr, uid, ids, context=context)
        res = {}
        for cruise_line in cruise_line_obj:
            total_price = 0
            for price_line in cruise_line.cruise_tour_sale_orde_price_line_ids:
                total_price += price_line.subtotal_price
            res[cruise_line.id] = total_price
        return res

    def _cost_total(self, cr, uid, ids, field, arg, context=None):
        """Calculates total cost from cost lines"""
        cruise_line_obj = self.browse(cr, uid, ids, context=context)
        res = {}
        for cruise_line in cruise_line_obj:
            total_cost = 0
            for cost_line in cruise_line.cruise_tour_sale_orde_price_line_ids:
                total_cost += cost_line.subtotal_cost
            res[cruise_line.id] = total_cost
        return res
    _columns={
            'product_id':fields.many2one('product.product', 'Product',
                domain=[('tour_category', '=','cruise')], mandatory=True),
#            'tour_id':fields.many2one('crm.lead', 'Lead'),
            'cruise_generic_url':fields.related('product_id',
                'cruise_generic_url', type='char', string='Generic Website',
                readonly=True),
            'cruise_tour_sale_orde_price_line_ids':\
                    fields.one2many('cruise.tour.sale.orde.price.line',
                'cruise_tour_sale_orde_line_id', 'Price Lines',
                help='Add price lines'),
            'cruise_price_total':fields.function(_price_total,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string = 'Price total ',
                help='Total sum of prices'),
            'cruise_cost_total':fields.function(_cost_total,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string = 'Cost total ',
                help='Total sum of costs'),
            }

    def onchange_product_id(self, cr, uid, ids, product, context=None):
        res = {}
        value = {}
        domain = {}
        context = context or {}
        if not product:
            return {'value':{'unit_price':0.0, 'unit_cost':0.0}}
        product_obj = self.pool.get('product.product')
        product_obj = product_obj.browse(cr, uid, product, context=context)
        value.setdefault('unit_price',product_obj.list_price)
        value.setdefault('unit_cost',product_obj.standard_price)
        ccto_ids = [ ccto.id for ccto in
                product_obj.cruise_cabin_ids ]
        domain.setdefault('cruise_cabin_id', [('id', 'in', ccto_ids)])
        res['value'] = value
        res['domain'] = domain
        return {'value':{'unit_price':product_obj.list_price,
            'unit_cost':product_obj.standard_price}}

    def button_dummy(self, cr, uid, ids, context=None):
        return True

#Lodge
class lodge_sale_order_line(osv.Model):
    _name="lodge.tour.sale.orde.line"
    _inherit="tour.sale.order.line"

    def _price_total(self, cr, uid, ids, field, arg, context=None):
        """Calculates total price from price lines"""
        lodge_line_obj = self.browse(cr, uid, ids, context=context)
        res = {}
        for lodge_line in lodge_line_obj:
            total_price = 0
            for price_line in lodge_line.lodge_tour_sale_orde_price_line_ids:
                total_price += price_line.subtotal_price
            res[lodge_line.id] = total_price
        return res

    def _cost_total(self, cr, uid, ids, field, arg, context=None):
        """Calculates total cost from cost lines"""
        lodge_line_obj = self.browse(cr, uid, ids, context=context)
        res = {}
        for lodge_line in lodge_line_obj:
            total_cost = 0
            for cost_line in lodge_line.lodge_tour_sale_orde_price_line_ids:
                total_cost += cost_line.subtotal_cost
            res[lodge_line.id] = total_cost
        return res

    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','lodge')]),
#            'tour_id':fields.many2one('crm.lead', 'Lead'),
            'lodge_tour_sale_orde_price_line_ids':fields.one2many('lodge.tour.sale.orde.price.line',
               'lodge_tour_sale_orde_line_id', 'Price line', help='Price Line'),
            'lodge_price_total':fields.function(_price_total,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string = 'Price total ',
                help='Total sum of prices'),
            'lodge_cost_total':fields.function(_cost_total,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string = 'Cost total ',
                help='Total sum of costs'),
            }

    def button_dummy(self, cr, uid, ids, context=None):
        return True
#Package
class package_sale_order_line(osv.Model):
    _name="package.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    def _price_total(self, cr, uid, ids, field, arg, context=None):
        """Calculates total price from price lines"""
        package_line_obj = self.browse(cr, uid, ids, context=context)
        res = {}
        for package_line in package_line_obj:
            total_price = 0
            for price_line in package_line.package_tour_sale_orde_price_line_ids:
                total_price += price_line.subtotal_price
            res[package_line.id] = total_price
        return res

    def _cost_total(self, cr, uid, ids, field, arg, context=None):
        """Calculates total cost from cost lines"""
        package_line_obj = self.browse(cr, uid, ids, context=context)
        res = {}
        for package_line in package_line_obj:
            total_cost = 0
            for cost_line in package_line.package_tour_sale_orde_price_line_ids:
                total_cost += cost_line.subtotal_cost
            res[package_line.id] = total_cost
        return res
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','package')]),
            'package_itinerary':fields.related('product_id', 'itinerary',
                string='Itinerary', help='Itenirary for package'),
#            'tour_id':fields.many2one('crm.lead', 'Lead'),
            'package_tour_sale_orde_price_line_ids':fields.one2many('package.tour.sale.orde.price.line',
                'package_tour_sale_orde_line_id', 'Price Line', help='Price Lines'),
            'package_price_total':fields.function(_price_total,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string = 'Price total ',
                help='Total sum of prices'),
            'package_cost_total':fields.function(_cost_total,
                method=True,
                type='float',
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string = 'Cost total ',
                help='Total sum of costs'),

            }
    def button_dummy(self, cr, uid, ids, context=None):
        return True
#Transfer
class transfer_sale_order_line(osv.Model):
    _name="transfer.tour.sale.orde.line"
    _inherit="tour.sale.order.line"

    def _total_line_price(self, cr, uid, ids, field_name, arg, context):
        result = {}
        lines = self.browse(cr, uid, ids, context)
        for l in lines:
            result[l.id] = l.unit_price * l.qtty
        return result

    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','transfer')]),
#            'tour_id':fields.many2one('crm.lead', 'Lead'),
            'transfer_total_line_price':fields.function(_total_line_price,
                method=True,
                store=False,
                fnct_inv=None,
                fnct_search=None,
                string='Total line price', help='Total transfer line price'),
            }
#Assistance
class assistance_sale_order_line(osv.Model):
    _name="assistance.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','assistance')]),
#            'tour_id':fields.many2one('crm.lead', 'Lead'),
            }
#Ticket
class ticket_sale_order_line(osv.Model):
    _name="ticket.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','fticket')]),
            'tour_id':fields.many2one('crm.lead', 'Lead'),
            'tour_ticket_info_ids':fields.one2many('tour.ticket.info',
                'ticket_tour_sale_orde_line_id', 'Ticket information line',
                help='Ticket information line'),
            }
#Miscellaneous
class misc_sale_order_line(osv.Model):
    _name="misc.tour.sale.orde.line"
    _inherit="tour.sale.order.line"
    _columns={
            'product_id':fields.many2one('product.product', 'Product',
                domain=[('tour_category', '=','misc')]),
#            'tour_id':fields.many2one('crm.lead', 'Lead'),
            }
#Accommodation
class accommodation_sale_order_line(osv.Model):
    _name="accommodation.tour.sale.orde.line"
    _inherit="tour.sale.order.line"


    _columns={
            'product_id':fields.many2one('product.product', 'Product', domain=[('tour_category', '=','accommodation')]),
#            'tour_id':fields.many2one('crm.lead', 'Lead'),
            'accommodation_room_type_id':fields.many2one(\
                "tour.accommodation.room.type", 'Accommodation Type',
                 required=True),
            }

    def onchange_product_id(self, cr, uid, ids, product, context=None):
        res = {}
        value = {}
        domain = {}
        context = context or {}
        if not product:
            return {'value':{'unit_price':0.0, 'unit_cost':0.0}}
        product_obj = self.pool.get('product.product')
        product_obj = product_obj.browse(cr, uid, product, context=context)
        value.setdefault('unit_price',product_obj.list_price)
        value.setdefault('unit_cost',product_obj.standard_price)
        arto_ids = [ arto.id for arto in
                product_obj.accommodation_room_type_ids ]
        domain.setdefault('accommodation_room_type_id', [('id', 'in', arto_ids)])
        res['value'] = value
        res['domain'] = domain

        return res

