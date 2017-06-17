from operation_service.utils.resource import Resource
class Ping(Resource):
    def get(self):
        return {"success":True}
