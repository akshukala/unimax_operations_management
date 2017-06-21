'''
    @author = Ganesh Bodkhe
    date = 2017-06-17 15:00
'''


from uni_db.inventory.models import Stock
from operation_service.utils.resource import Resource

class InventoryStock(Resource):
    def get(self):
    	response = [{'product_id': str(stock.id),
                     'product_name':str(stock.product.product_name),
                     'quantity':str(stock.quantity),
                     'fulfilled_qty':str(stock.fulfilled_qty)} for stock in Stock.objects.filter(product__active=True)]
        return response