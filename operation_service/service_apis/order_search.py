'''
    @author = Akshay Kale
    date = 2017-06-17 15:00
'''

from flask.globals import request
from datetime import datetime
from operation_service.utils.resource import Resource
from operation_service.service_api_handlers import get_orders_handler
from uni_db.order_management.models import Order, Transaction


class OrderSearch(Resource):

    def get(self):
        data = request.args.to_dict()
        return get_orders_handler.handle_order_request(data)

    def post(self):
        request_data = request.get_json(force=True)
        ord_obj = Order.objects.get(sales_order_id=int(request_data.get('order_id')))
        if str(request_data['order_status']) == 'ORDER COMPLETED':
            pay_date = datetime.strptime(str(request_data['pay_dt'])+' 0:0:0',
                                         '%Y-%m-%d %H:%M:%S')
            if(Transaction.objects.filter(order=ord_obj).exists()):
                trans_obj = Transaction.objects.get(order=ord_obj)
                trans_obj.payment_mode = str(request_data.get('payment_mode'))
                trans_obj.transaction_note = str(request_data.get('note'))
                trans_obj.payment_date = pay_date
                trans_obj.bank = str(request_data.get('bank'))
                trans_obj.save()
            else:
                Transaction.objects.create(payment_mode=str(request_data.get('payment_mode')),
                                           transaction_note=str(request_data.get('note')),
                                           payment_date=pay_date,
                                           bank=str(request_data.get('bank')),
                                           order=ord_obj)
        else:
            if(Transaction.objects.filter(order=ord_obj).exists()):
                trans_obj = Transaction.objects.get(order=ord_obj)
                trans_obj.payment_mode = str(request_data.get('payment_mode'))
                trans_obj.transaction_note = str(request_data.get('note'))
                trans_obj.bank = str(request_data.get('bank'))
                trans_obj.save()
            else:
                Transaction.objects.create(payment_mode=str(request_data.get('payment_mode')),
                                           transaction_note=str(request_data.get('note')),
                                           bank=str(request_data.get('bank')),
                                           order=ord_obj)
        
        ord_obj.status = str(request_data.get('order_status'))
        ord_obj.save()
        return "Success"
