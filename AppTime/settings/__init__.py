import socket
from .base_settings import *

local_hosts = ['MacBook-Pro-Kasper.local']

if socket.gethostname() in local_hosts:
    from .local_settings import *
else:
    from .production_settings import *
