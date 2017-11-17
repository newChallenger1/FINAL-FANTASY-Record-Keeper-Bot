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
		
	def callAPI(self,path,kind,data=None):
		if kind ==1:
			r=self.s.get(self.base+path)
		else:
			r=self.s.post(self.base+path,data=data)
		return r.content
		
	def create_session(self):
		data={}
		data['userId']=self.userId
		data['accessToken']=self.accessToken
		return self.callAPI('/dff/_api_create_session',2,data)
		
	def update_user_session(self):
		self.s.headers.update({'X-Requested-With':'XMLHttpRequest','User-Session':'UNDEFINED_IN_API_JS','X-CSRF-Token':self.csrf})
		res= self.callAPI('/dff/update_user_session',2,json.dumps({}))
		self.user_session_key=json.loads(res)['user_session_key']
		self.s.headers.update({'App-Js-Version':self.appJsVersion,'User-Session':self.user_session_key})
		return res
		
	def setValues(self,input):
		self.csrf=re.search('FFEnv.csrfToken="(.*)";',input).group(1)
		self.appJsVersion=re.search("FFEnv.appJsVersion='(.*)';",input).group(1)
		
	def splash(self):
		return self.callAPI('/dff/splash',1)
		
	def init(self):
		return self.callAPI('/dff/',1)

	def tutorial_proceed(self,step):
		data={}
		data['step']=int(step)
		return self.callAPI('/dff/tutorial/proceed',2,data)

	def create_nickname(self,name):
		data={}
		data['nickname']=name
		return self.callAPI('/dff/tutorial/create_nickname',2,data)
		
	def tutorial_battles(self):
		return self.callAPI('/dff/tutorial/battles',2,json.dumps({}))

	def login_bonus(self):
		return self.callAPI('/dff/login_bonus/receive',2,json.dumps({}))

	def tutorial_give_and_set_ability(self):
		return self.callAPI('/dff/tutorial/give_and_set_ability',2,json.dumps({}))

	def tutorial_begin_battle_session(self,step):
		data={}
		data['step']=int(step)
		return self.callAPI('/dff/tutorial/begin_battle_session',2,data)

	def tutorial_battle_win(self):
		data={}
		data['results']='jkm7henLBaW9Otc7T1vh3zigmM0WRlj27WXh2R45p1TLfLL1FlD1AsgJ53upTSkhYSL/3m4HsPzIR0DcGQ/8LDc/3/Yyp5i4whlwUw2SAzUUqM9jWC1OG49Tv0gUvYSczuEd3Spqicf90u86ZNGgIhodnlpIcVjyaLB/lETrBc8=_P9l2alLr4m81+iIrRsc7JJ2iYnT74M7kwReha0s4qwi+bUAwjwe2HbYg2ZhfjizDx4GT9Xm/GgpfRqbd8c7HrsUACxCLc37Ctg9jUKWUabYdvLVLvqkkFEbS26m9AFsYP45tgenvx5LTDkDjI/GxTZQVP3rDG8WzTo0tbuHbunmcb/vcXdkJerUZvyzxrfmROhCHToulIr7u0fqyx1j7WotTqznkmHxadMDRQa+CuQC/JoSS//f6Jm+TjtEvxQW6iQ4DWt2TN/ElCyJgnWyV5M6/QZlh0Ezzl9edks3cjqEQ1E09ohaem16lz0tqlDC5B4Y6cp2WWbR3zfg1R1lkZDrhkmnMYhkmTZqq/V8llEhR4L5ALVkJQ6hglEksOxtRWj2orO/JK/ZCoZQ9rd9jkJl2oRpQleimaiFBpaQTzXdyS9DcZ/9zDWVyu2sXi13hJPXm6xL/xidWgtGDIO2gGDkXv+rGpPclmCuSJS6UJQaPbsE6qaPPMRg02SxJZGn2Tnx9LjRH8df6F3zQ7/oxp/4xYeab0VB6uWD0dFhXxV9A/KJxxgbjVter4w0PM3Y/cBQ2uCVAJQQH+uTAzqjvxHnxRvON8FtTyM/92fuYxSFDIKavcZsGdxxNat/+M2TpmYf0KxWn1tDn0tZ2opnn9MJoMKgUUVnXXvYhWMfTP7fVGo4ZUCfxhvN8oxppEwOg0dCo3k31iZwvw+Gv7I2hoJ9F9rRSWKuKmyt4bWlKR9D8aUTTFh9qL18THKNvSf4FRTePJvYfTpP9erzTmfJoSO9v1GsaotYBUALu02YZLMsY3x6mWFG+A8N5YlOGxzD3szFh1R9w+rcwTZ2jwriZ1b7+7bdZtzrySkfmHpc5tb1Je/kZXXHUk4FtiVOV4Q9SgPO3t5ZpiaK2NF5kQTu6HrcY1PDNz2Oo35hdS1B0vMq4dvxE1ZFu2LkRMr+0aFcKao6rhMm9rD4AzzsCqVOpXlzkgqYrglHR2uvb12R7VZs='
		return self.callAPI('/dff/tutorial/battle_win',2,data)

	def tutorial_battle_init_data(self):
		return self.callAPI('/dff/tutorial/get_battle_init_data',1)
		
	def tutorial_gacha_list(self):
		return self.callAPI('/dff/tutorial/gacha_list',1)
		
	def TS10(self):
		return str(int(time.time()))
		
	def tutorial(self):
		res= self.callAPI('/dff/tutorial/?timestamp=%s'%(self.TS10()),1)
		self.user_data=json.loads(re.search('<script data-app-init-data type="application/json">(.*)</script>',res).group(1))
		return res

	def tutorial_update_rcommend_party(self):
		data={"step":100,"slot_to_buddy_id":{"1":49760529,"2":49760530,"3":49760531,"4":0,"5":0},"changed_row_info":{"49760530":2,"49760531":2}}
		return self.callAPI('/dff/tutorial/update_recommend_party',2,data)

	def tutorial_execute_gacha(self,step):
		data={}
		data['step']=int(step)
		return self.callAPI('/dff/tutorial/execute_gacha',2,data)

	def tutorial_update_hero_equipment(self,step,equip_id):
		data={}
		data['step']=int(step)
		data['equipment_id']=int(equipment_id)
		return self.callAPI('/dff/tutorial/update_hero_equipment',2,data)

	def completeTutorial(self):
		self.tutorial_proceed(0)
		self.tutorial_proceed(4)
		self.create_nickname('Mila432')
		self.tutorial_proceed(6)
		self.tutorial_proceed(10)
		self.create_session()
		self.splash()
		self.tutorial_proceed(20)
		self.tutorial_proceed(30)
		self.tutorial_proceed(40)
		self.tutorial_proceed(49)
		self.tutorial_proceed(58)
		self.tutorial_battles()
		self.tutorial_begin_battle_session(70)
		self.tutorial_battle_init_data()
		exit(1)#TODO
		self.tutorial_battle_win()
		self.tutorial()
		self.tutorial_proceed(90)
		self.tutorial_update_rcommend_party()
		self.tutorial_gacha_list()
		self.tutorial_execute_gacha(110)
		self.tutorial_proceed(120)
		self.tutorial_proceed(130)
		self.tutorial_proceed(150)
		self.tutorial_update_hero_equipment(160,774547918)
		self.tutorial_give_and_set_ability()
		self.tutorial_proceed(183)
		self.tutorial_proceed(185)
		self.tutorial_proceed(186)
		self.tutorial_proceed(187)
		self.tutorial_proceed(190)
		self.tutorial_proceed(200)
		
	def login(self):
		res=self.create_session()
		self.user_id=json.loads(res)['id']
		self.setValues(self.splash())
		self.init()
		self.update_user_session()

if __name__ == "__main__":
	a=API()
	a.setUser(Tools().rndDeviceId())
	a.login()
	a.completeTutorial()