import xmlrpc.client
s = xmlrpc.client.ServerProxy('http://localhost:9000')
print(s.len("Tutorialspoint"))
print(s.rmndr(12,5))
print(s.modl(7,3))
# Print list of available methods
print(s.system.listMethods())