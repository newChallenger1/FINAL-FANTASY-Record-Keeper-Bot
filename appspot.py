import requests
import re
import sys
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Appspot(object):
	def __init__(self):
		self.s=requests.session()
		self.s.verify=False
		self.s.headers.update({'Content-Type':'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B93'})
		if 'win' in sys.platform:
			self.s.proxies.update({'http': 'http://127.0.0.1:8888','https': 'https://127.0.0.1:8888',})
		self.bundleId='com.dena.west.FFRK'
		self.storeName='APPLE'
		self.sdkVersion='iOS-2.3.0-339e83c'
		self.app_version='5.3.1'
		self.rcp='com.dena.west.lcd.web.client.rpc.WebRemoteService'
		self.id=None
		self.token=None
		self.userId=None
		self.u1=None

	def setId(self,device_id,push_token=None,u1=None):
		self.device_id=device_id
		self.push_token=push_token if push_token else '0000000000000000000000000000000000000000000000000000000000000000'
		if u1:
			self.u1=u1

	def callAPI(self,path,kind,data=None):
		if kind == 1:
			r=self.s.get(path)
		else:
			r=self.s.post(path,data=data)
		return r.content

	def createSession(self):
		self.callAPI('https://lcd-prod.appspot.com/LCDWeb.html?action=createSession&locale=en_DE',1)
		self.setPremutation(self.callAPI('https://lcd-prod.appspot.com/lcdweb/lcdweb.nocache.js',1))
		return self.premutation
	
	def callPremutation(self):
		return self.callAPI('https://lcd-prod.appspot.com/lcdweb/%s.cache.js'%(self.premutation),1)
	
	def getTS13(self):
		return str(int(time.time()*1000))

	def getStoreType(self):
		pre=self.callPremutation()
		self.s.headers.update({'X-GWT-Module-Base':'https://lcd-prod.appspot.com/lcdweb/','Accept-Language':'en-us','X-GWT-Permutation':self.premutation,'Content-Type':'text/x-gwt-rpc; charset=UTF-8','Origin':'https://lcd-prod.appspot.com','Referer':'https://lcd-prod.appspot.com/LCDWeb.html?action=createSession&locale=en_DE'})
		self.setE(pre)
		data='7|0|18|https://lcd-prod.appspot.com/lcdweb/|%s|%s|getStoreType|com.dena.west.lcd.web.shared.model.Capabilities/399814386|00000000-0000-0000-0000-000000000000|%s|%s|Mila432|iPhone10,6|%s|en_DE|Apple|wifi|11.1|%s|APPLE|Europe/Berlin|1|2|3|4|1|5|5|0|6|7|8|9|0|568|10|11|320|0|0|0|0|12|13|14|15|0|0|16|0|0|17|18|3600000|'%(self.E,self.rcp,self.app_version,self.bundleId,self.push_token,self.sdkVersion)
		return self.callAPI('https://lcd-prod.appspot.com/lcdweb/rpc/getStoreType?bundleId=%s&storeName=%s&sdkVersion=%s&t=%s'%(self.bundleId,self.storeName,self.sdkVersion,self.getTS13()),2,data)
	
	def createNewSession(self,loadOld):
		if not loadOld:
			data='7|0|19|https://lcd-prod.appspot.com/lcdweb/|%s|%s|createNewSession|com.dena.west.lcd.web.shared.model.Capabilities/399814386|com.dena.west.lcd.web.shared.model.Credentials/2571271145|00000000-0000-0000-0000-000000000000|%s|%s|Mila432|iPhone10,6|%s|en_DE|Apple|wifi|11.1|%s|APPLE|Europe/Berlin|1|2|3|4|2|5|6|5|0|7|8|9|10|0|568|11|12|320|0|0|0|0|13|14|15|16|0|0|17|0|0|18|19|3600000|6|0|0|0|0|0|0|0|0|0|0|'%(self.E,self.rcp,self.app_version,self.bundleId,self.push_token,self.sdkVersion)
		else:
			data='7|0|21|https://lcd-prod.appspot.com/lcdweb/|%s|%s|createNewSession|com.dena.west.lcd.web.shared.model.Capabilities/399814386|com.dena.west.lcd.web.shared.model.Credentials/2571271145|00000000-0000-0000-0000-000000000000|%s|%s|Mila432|iPhone10,6|%s|en_DE|Apple|wifi|11.1|%s|APPLE|Europe/Berlin|%s|%s|1|2|3|4|2|5|6|5|0|7|8|9|10|0|568|11|12|320|0|0|0|0|13|14|15|16|0|0|17|0|0|18|19|3600000|6|0|0|0|0|20|21|0|0|0|0|'%(self.E,self.rcp,self.app_version,self.bundleId,self.push_token,self.sdkVersion,self.device_id,self.u1)
		res=self.callAPI('https://lcd-prod.appspot.com/lcdweb/rpc/createNewSession?bundleId=%s&storeName=%s&sdkVersion=%s&t=%s'%(self.bundleId,self.storeName,self.sdkVersion,self.getTS13()),2,data)
		self.token=re.search('","(.{400,470})","',res).group(1)
		self.userId=re.search('","([0-9]{15,15})","',res).group(1)
		return res

	def getAccessToken(self):
		return self.token

	def getUserId(self):
		return self.userId
	
	def setE(self,input):
		self.E=re.search("this.e='(.{32,32})'}",input).group(1)

	def setPremutation(self,input):
		self.premutation=re.search("',jd='(.{32,32})',kd",input).group(1)
