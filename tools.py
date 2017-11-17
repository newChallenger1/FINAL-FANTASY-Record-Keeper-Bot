import random

class Tools(object):
	def __init__(self):
		pass
		
	def rndHex(self,n):
		return ''.join([random.choice('0123456789ABCDEF') for x in range(n)])
	
	def rndDeviceId(self):
		s='%s-%s-%s-%s-%s'%(self.rndHex(8),self.rndHex(4),self.rndHex(4),self.rndHex(4),self.rndHex(12))
		return s.lower()