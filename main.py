import socket

import importlib
import settings

role_module = importlib.import_module('roles.{}.{}'.format(settings.Roles.hosts[socket.gethostname()],'main'))
