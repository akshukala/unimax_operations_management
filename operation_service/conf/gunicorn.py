import os

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

bind = "127.0.0.1:7287"
workers = numCPUs() * 2 + 1
backlog = 2048
worker_class ="gevent"
debug = True
daemon = False
pidfile ="/tmp/operationservice-gunicorn.pid"
logfile ="/tmp/operationservice-gunicorn.log"
loglevel = 'info'
accesslog = '/tmp/gunicorn-access.log'

