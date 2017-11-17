import json
import requests
import sys
import re
import time
import random
from appspot import Appspot
from tools import Tools

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class API(object):
	def __init__(self):
		self.s=requests.session()
		self.s.verify=False
		self.s.headers.update({'Content-Type':'application/x-www-form-urlencoded','User-Agent':'DotFFWWMOPS/531 CFNetwork/811.4.18 Darwin/16.5.0'})
		if 'win' in sys.platform:
			self.s.proxies.update({'http': 'http://127.0.0.1:8888','https': 'https://127.0.0.1:8888',})
		self.base='https://ffrk.denagames.com'
		self.appspot=Appspot()
		self.tools=Tools()
		
	def setUser(self,device_id,push_token=None):
		self.appspot.setId(device_id,push_token)
		self.appspot.createSession()
		self.appspot.getStoreType()
		self.appspot.createNewSession()
		self.userId=self.appspot.getUserId()
		self.accessToken=self.appspot.getAccessToken()
		print self.userId,self.accessToken
		
	def callAPI(self,path,data):
		return self.s.post(self.base+path,data=data).content
		
	def create_session(self):
		data={}
		data['userId']=self.userId
		data['accessToken']=self.accessToken
		return self.callAPI('/dff/_api_create_session',data)
		
if __name__ == "__main__":
	a=API()
	a.setUser(Tools().rndDeviceId())
	print a.create_session()