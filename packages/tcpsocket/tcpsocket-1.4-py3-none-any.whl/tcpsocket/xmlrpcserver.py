from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
class RequestHandler(SimpleXMLRPCRequestHandler):
   rpc_paths = ('/RPC2',)
with SimpleXMLRPCServer(('localhost', 9000),
                        requestHandler=RequestHandler) as server:
   server.register_introspection_functions()
   # Register len() function;
   server.register_function(len)
   # Register a function under a different name
   @server.register_function(name='rmndr')
   def remainder_function(x, y):
      return x // y
   # Register a function under function.__name__.
   @server.register_function
   def modl(x, y):
      return x % y
   server.serve_forever()