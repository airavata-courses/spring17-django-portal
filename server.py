import wsgiserver
import sys
import os
from PortalPOC import  settings
from django.core.wsgi import get_wsgi_application
import json
CACHE_ENABLED=True



port=8000
if len(sys.argv) > 1:
    port=int(sys.argv[1])

if len(sys.argv) > 2:
    CACHE_ENABLED=json.loads(sys.argv[2])

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'PortalPOC.settings'
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    print('Port: '+str(port))
    server=wsgiserver.WSGIServer(get_wsgi_application(),host='127.0.0.1',port=port)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
