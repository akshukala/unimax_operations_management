
'''
    @author = Akshay Kale
    date = 2017-06-17 15:00
'''

from flask import current_app as app
from flask.globals import request
from operation_service.utils.resource import Resource
from uni_db.order_management.models import Order, OrderItem
from uni_db.inventory.models import Delivery, Stock
from operation_service.service_api_handlers import get_orders_handler


class SaleOrders(Resource):

    def get(self):
        data = request.args.to_dict()
        return get_orders_handler.handle_request(data)

    def post(self):
        '''Creating delivery by object and setting delivery by value'''
        request_data = request.get_json(force=True)
        delivery_by = str(request_data.get('delivery_by')).strip()
        order_id = int(request_data.get('orderid'))
        order = Order.objects.get(sales_order_id=order_id)
        if(Delivery.objects.filter(order=order_id).exists()):
            Delivery.objects.filter(order=order
                                    ).update(delivery_by=delivery_by)
        else:
            Delivery.objects.create(delivery_by=delivery_by, order=order)

        return "Success"

    def put(self):
        request_data = request.get_json(force=True)
        order_id = int(request_data.get('order_id'))

        if Delivery.objects.filter(order=Order.objects.get(sales_order_id=
                                                           order_id)).exists():
            order_obj = Order.objects.get(sales_order_id=order_id)
            order_obj.status = 'FULFILLABLE'
            order_obj.save()
            orderitem_obj = OrderItem.objects.filter(order=order_obj)
            for oi in orderitem_obj:
                orderitem = oi.item_name.split('-')
                inventory_obj = Stock.objects.get(product=int(orderitem[0]))
                fulfilled_count = inventory_obj.fulfilled_qty
                inventory_obj.fulfilled_qty = int(fulfilled_count
                                                  ) + int(oi.quantity)
                inventory_obj.save()
            return {"responseCode": 200,
                    "Message": "Order Successfully Fulfilled. "
                    }
        else:
            return {"responseCode": 400,
                    "Message": "Delivery object not created"
                    }