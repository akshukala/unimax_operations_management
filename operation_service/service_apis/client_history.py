from django.core.exceptions import ObjectDoesNotExist
from flask import current_app as app
from flask.globals import request
from dateutil.parser import parse
import requests

from uni_db.order_management.models import Order, OrderItem
from uni_db.client_erp.models import ClientMobile
from operation_service.utils.resource import Resource
from operation_service.utils.address_utils import address_as_json


class ClientHistory(Resource):

    def get(self):
        response = []
        orders = Order.objects.get(sales_order_id=int(request.args.get('order_id')))
        order_dict = {}
        order_dict['order_id'] = orders.sales_order_id
        order_dict['client_id'] = orders.owner.client_id
        order_dict['clientname'] = orders.owner.client_name
        mobile_nos = ''
        for mob in ClientMobile.objects.filter(client=orders.owner):
            mobile_nos += str(mob.mobile) + ","
        order_dict['mobile_no'] = mobile_nos
        order_dict['address'] = address_as_json(orders.billing_address)
        order_dict['status'] = orders.status
        order_dict['created_by'] = orders.entered_by.username
        order_dict['cod_amt'] = orders.cod_amount
        order_dict['created_date'] = (orders.created_on).strftime("%d/%m/%Y")
        order_dict['discount'] = orders.total_discount
        orderItemList = []
        orderQuantityList = []
        itemSellingPrice = []
        for oi in OrderItem.objects.filter(order=orders):
            itemname = oi.item_name.split('-')
            orderItemList.append(itemname[1])
            orderQuantityList.append(oi.quantity)
            itemSellingPrice.append(oi.selling_price)
        order_dict['orderitems'] = orderItemList
        order_dict['quantity'] = orderQuantityList
        order_dict['selling_price'] = itemSellingPrice
        response.append(order_dict)

        order_history = Order.objects.filter(owner__client_name=
                                             orders.owner.client_name
                                             ).exclude(status='CANCELLED')
        for order_his in order_history:
            order_hist_dict = {}
            order_hist_dict['order_id'] = str(order_his.sales_order_id)
            order_hist_dict['created_by'] = order_his.entered_by.username
            order_hist_dict['created_date'] = (order_his.created_on
                                               ).strftime("%d/%m/%Y")
            order_hist_dict['cod_amt'] = order_his.cod_amount
            order_hist_dict['status'] = order_his.status
            response.append(order_hist_dict)
        return response