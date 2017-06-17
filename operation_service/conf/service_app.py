from uni_db.settings.pool import init_pool
from os.path import dirname, abspath

import django
from django.db import close_old_connections
from flask import Flask
from flask.ext import restful

from operation_service.conf.config_logger_setup import setup_config_logger
from operation_service.session.interfaces import DBInterface
from flask.ext.cors import CORS
from operation_service.service_apis.ping import Ping


close_old_connections()
init_pool()

django.setup()
app = Flask(__name__)
CORS(app)
app.auth_header_name = 'X-Authorization-Token'
app.session_interface = DBInterface()
app.root_dir = dirname(dirname(abspath(__file__)))

api = restful.Api(app)

setup_config_logger(app)

app.logger.info("Setting up Resources")
api.add_resource(Ping, '/operationservice/ping/')

app.logger.info("Resource setup done")

if __name__ == '__main__':
    # from gevent import monkey
    # from crmadminservice.utils.hacks import gevent_django_db_hack
    # gevent_django_db_hack()
    # monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False, aggressive=True)
    app.run(host="0.0.0.0", port=7287,threaded=True)
