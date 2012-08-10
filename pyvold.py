from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

import voldemort

# connection to Voldemort
client = voldemort.StoreClient('test', [('localhost', 6666)])

def getGETKeys(request):
	# take the first arg as key to read
	return map(str, request.GET.keys()) if request.GET else None

@view_config(route_name='kvroute', request_method='GET', renderer='text', http_cache=0)
def getKeys(request):
	keys = getGETKeys(request)
	# if no key given, key blank, etc.
	if not keys:
		return Response("Welcome to pyvold!\n")
	vold_resp = client.get_all(keys)
	# Take the first value(s), ignore versioning for now
	str_vold_resp = str(dict([(key, vold_resp[key][0][0]) for key in vold_resp])) if vold_resp else None;
	print(str_vold_resp)
	return Response(str_vold_resp + "\n" if str_vold_resp else 'not found\n')

@view_config(route_name='kvroute', request_method='POST', renderer='text', http_cache=0)
def postKey(request):
	if not request.POST:
		return Response("Error: no key specified\n")
	key, value = [str(x) for x in request.POST.items()[0]]
	client.put(key, value)
	print key + " => " + value
	return Response(key + " => " + value + "\n")

@view_config(route_name='kvroute', request_method='PUT', renderer='text', http_cache=0)
def putKey(request):
	# We don't distinguish create and update
	return postKey(request)

@view_config(route_name='kvroute', request_method='DELETE', renderer='text', http_cache=0)
def delKey(request):
	key = getGETKeys(request)
	if not key:
		return Response("Error: no key specified\n")
	resp = client.delete(key)
	return Response("deleted '" + key + "'\n") if resp else Response("not found\n")

if __name__ == '__main__':
	config = Configurator()
	config.add_route('kvroute', '/')
	config.scan()

	app = config.make_wsgi_app()
	server = make_server('0.0.0.0', 8080, app)
	server.serve_forever()
