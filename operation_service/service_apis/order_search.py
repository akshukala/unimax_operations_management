'''
    @author = Akshay Kale
    date = 2017-06-17 15:00
'''

from flask import current_app as app
from flask.globals import request
from operation_service.utils.resource import Resource
from operation_service.service_api_handlers import get_orders_handler
from uni_db.order_management.models import Order


class OrderSearch(Resource):

    def get(self):
        data = request.args.to_dict()
        return get_orders_handler.handle_order_request(data)

    def put(self):
        request_data = request.get_json(force=True)
        ord_obj = Order.objects.get(sales_order_id=int(request_data.get('order_id')))
        ord_obj.sales_order_id
        ord_obj.status = str(request_data.get('order_status'))
        ord_obj.save()
        return "Success"