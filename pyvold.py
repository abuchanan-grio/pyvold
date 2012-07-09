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

@view_config(route_name='kvroute', request_method='GET', renderer='text', http_cache=0)
def getKey(request):
	key = getGETKey(request)
	# if no key given, key blank, etc.
	if not key:
		return Response("Welcome to pyvold!\n")
	
	vold_resp = client.get(key)
	# Take the first response, ignore versioning for now
	str_vold_resp = vold_resp[0][0] if vold_resp else None;
	return Response(str_vold_resp + "\n" if str_vold_resp else 'not found\n')

@view_config(route_name='kvroute', request_method='POST', renderer='text', http_cache=0)
def postKey(request):
	if not request.POST:
		return Response("Error: no key/value specified\n")
	key, value = [str(x) for x in request.POST.items()[0]]
	client.put(key, value)
	return Response(key + " => " + value + "\n")

@view_config(route_name='kvroute', request_method='PUT', renderer='text', http_cache=0)
def putKey(request):
	# We don't distinguish create and update
	return postKey(request)

@view_config(route_name='kvroute', request_method='DELETE', renderer='text', http_cache=0)
def delKey(request):
	key = getGETKey(request)
	if not key:
		return Response("Error: no key/value specified\n")
	resp = client.delete(key)
	return Response("deleted " + key + "\n") if resp else Response("not found\n")

if __name__ == '__main__':
	config = Configurator()
	config.add_route('kvroute', '/')
	config.scan()

	app = config.make_wsgi_app()
	server = make_server('0.0.0.0', 8080, app)
	server.serve_forever()
