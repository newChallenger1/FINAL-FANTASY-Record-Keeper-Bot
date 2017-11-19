from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
import rsa
from Crypto import Random
from pkcs7 import PKCS7Encoder
import base64
import os

class Crypter(object):
	def __init__(self):
		self.publicKey='''-----BEGIN PUBLIC KEY-----
						MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDmP7wDzgRS9xH8iSFFFTm7H2NI
						WrgQ+AtXmXLesgGQpmKMzLr/HiivvLCgEJduaDc1h8vgwge6GpbXKEbwCOe8kxR+
						jz93WWbEJl8j3AULM8gLoGMorknamzSH9CwatXXOcJexKMDYW7vq4ih0tFwrV1Sz
						FdycelH7J6YDWOC8zQIDAQAB
						-----END PUBLIC KEY-----'''

	def setSeed(self,key=None):
		if not key:
			key=self.genSeed()
			print 'using random key %s'%(key.encode('hex'))
		elif len(key)>=33:
			key=key.replace(' ','').decode('hex')
		self.key=key

	def rsaEncryptText(self):
		#pubkey = RSA.importKey(self.publicKey)
		#pubkey = PKCS1_v1_5.new(pubkey)
		#print 'rsaEncryptText:%s'%self.key.encode('hex')
		#return base64.b64encode(pubkey.encrypt(self.key)).replace('\n','')
		#print rsa.common.byte_size(rsa.PublicKey.load_pkcs1_openssl_pem(self.publicKey).n)
		res=rsa.encrypt(self.key, rsa.PublicKey.load_pkcs1_openssl_pem(self.publicKey))
		return base64.b64encode(res)

	def genSeed(self):
		return os.urandom(16)

	def encrypt(self,raw):
		raw = raw + '\x00' * ((16 - (len(raw) % 16)) % 16)
		cipher = AES.new(self.key,AES.MODE_ECB)
		return base64.b64encode(cipher.encrypt(raw))

	def decrypt(self,enc):
		enc = base64.b64decode(enc)
		cipher = AES.new(self.key, AES.MODE_ECB)
		return PKCS7Encoder().decode(cipher.decrypt(enc))