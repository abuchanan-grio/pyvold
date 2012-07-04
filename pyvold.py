from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import json

import voldemort

from IPython import embed

# connection to Voldemort
client = voldemort.StoreClient('test', [('localhost', 6666)])

def getGETKey(request):
	# take the first arg as key to read
	return str(request.GET.keys()[0]) if request.GET else None

@view_config(route_name='kvroute', request_method='GET', renderer='json', http_cache=0)
def getKey(request):
	key = getGETKey(request)
	# if no key given, key blank, etc.
	if not key:
		return Response("Welcome to pyvold!")
	
	vold_resp = client.get(key)
	# Take the first response, ignore versioning for now
	str_vold_resp = vold_resp[0][0] if vold_resp else None;
	return Response(json.dumps(str_vold_resp))

@view_config(route_name='kvroute', request_method='POST', renderer='json', http_cache=0)
def putKey(request):
	if not request.POST:
		return Response("Error: no key/value specified")
	key, value = [str(x) for x in request.POST.items()[0]]
	client.put(key, value)
	return Response(key + " => " + value)

@view_config(route_name='kvroute', request_method='DELETE', renderer='json', http_cache=0)
def delKey(request):
	key = getGETKey(request)
	if not key:
		return Response("Error: no key/value specified")
	resp = client.delete(key)
	return Response("deleted " + key) if resp else Response("not found")

if __name__ == '__main__':
	config = Configurator()
	config.add_route('kvroute', '/')
	config.scan()

	app = config.make_wsgi_app()
	server = make_server('0.0.0.0', 8080, app)
	server.serve_forever()
