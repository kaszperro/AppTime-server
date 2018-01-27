import socket
from .base_settings import *

local_hosts = ['MacBook-Pro-Kasper.local']

if socket.gethostname() in local_hosts:
    print("local")
    from .local_settings import *
else:
    print("production")
    from .production_settings import *
