'''
    @author = Akshay Kale
'''

from uni_db.order_management.models import (
    Order, OrderItem
)
from uni_db.inventory.models import Delivery, Stock
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operation_service.utils.address_utils import address_as_json


def get_orders(paginator_obj):
    response = []
    for order in paginator_obj:
        order_dict = {}
        order_dict['order_id'] = str(order.sales_order_id)
        order_dict['client_id'] = str(order.owner.client_id)
        order_dict['client_name'] = str(order.owner.client_name)
        order_dict['address'] = address_as_json(order.billing_address)
        order_dict['status'] = str(order.status)
        order_dict['internal_note'] = str(order.internal_note)
        order_dict['amount'] = str(order.cod_amount)
        order_dict['created_date'] = (order.created_on).strftime("%d/%m/%Y")
        orderItemList = []
        orderItemid = []
        orderQuantityList = []
        remaining_stk = []
        fulfilled_stk = []
        for oi in OrderItem.objects.filter(order=order):
                            itemname = oi.item_name.split('-')
                            orderItemList.append(itemname[1])
                            orderItemid.append(itemname[0])
                            orderQuantityList.append(oi.quantity)
        order_dict['orderitems'] = orderItemList
        order_dict['quantity'] = orderQuantityList
        try:
            delivery_obj = Delivery.objects.get(order=order)
            order_dict['delivery_by'] = str(delivery_obj.delivery_by)
            order_dict['delivery_challan'] = str(delivery_obj.delivery_chalan)
            order_dict['driver_name'] = str(delivery_obj.driver_name)
        except ObjectDoesNotExist:
                order_dict['delivery_by'] = "Not Decided as object not created"
        for orderItem in orderItemid:
            if(Stock.objects.filter(product__id=int(orderItem)).exists()):
                stock = Stock.objects.get(product__id=int(orderItem))
                remaining_stk.append((int(stock.quantity)-int(stock.fulfilled_qty)))
                fulfilled_stk.append(int(stock.fulfilled_qty))
            else:
                order_dict['remaining_stock'] = "Product Stock not available"
        order_dict['remaining_stock'] = remaining_stk
        order_dict['fulfilled_qty'] = fulfilled_stk
        response.append(order_dict)
    return response


def handle_request(data):
    try:
        if str(data.get('status')) == "ALL":
            order_obj = Order.objects.all().exclude(status='CANCELLED')
        else:
            order_obj = Order.objects.filter(status=str(data.get('status')))
        paginator = Paginator(order_obj, 2)
        try:
            paginator_obj = paginator.page(str(data.get('page')))
            response_data = get_orders(paginator_obj)
            response_data.append(len(order_obj))
            response_data.append(int(paginator.num_pages))
            return response_data
        except PageNotAnInteger:
            '''# If page is not an integer, deliver first page.'''
            paginator_obj = paginator.page(1)
            response_data = get_orders(paginator_obj)
            return response_data
        except EmptyPage:
            '''# If page is out of range (e.g. 9999), deliver
                last page of results.'''
            paginator_obj = paginator.page(paginator.num_pages)
    except ObjectDoesNotExist:
        return
        {
         'errorCode': 503,
         'errorMessage': "Orders not available."
        }


def handle_order_request(data):
    if(str(data.get('type')) == 'Name'):
        try:
            data = str(data.get('data'))
            order_obj = Order.objects.filter(owner__client_name__icontains=data)
            return get_orders(order_obj)
        except ObjectDoesNotExist:
            return {"responseCode": 400,
                    "Message": "No such Client exists"}
    elif str(data.get('type')) == 'Order':
        try:
            data = int(data.get('data'))
            order_obj = Order.objects.filter(sales_order_id=data)
            return get_orders(order_obj)
        except ObjectDoesNotExist:
            return {"errorCode": 200,
                    "errorMessage": "Wrong Order Id"}
    else:
        return {"responseCode": 200,
                "Message": "Wrong Search Term"}
