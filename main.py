import json
import requests
import sys
import re
import time
import random
import datetime
from appspot import Appspot
from tools import Tools
from crypt import Crypter

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
		self.crypter=Crypter()
		self.begin_token=None
		self.battle_session_key=None

	def setUser(self,device_id,push_token=None,u1=None):
		self.appspot.setId(device_id,push_token,u1)
		self.appspot.createSession()
		self.appspot.getStoreType()
		self.appspot.createNewSession(True if u1 else False)
		self.userId=self.appspot.getUserId()
		self.accessToken=self.appspot.getAccessToken()
		#print self.userId,self.accessToken

	def callAPI(self,path,kind,data=None):
		if kind ==1:
			self.s.headers.update({'Content-Type':'application/x-www-form-urlencoded'})
			r=self.s.get(self.base+path)
		else:
			if type(data) <> str:
				self.s.headers.update({'Content-Type':'application/x-www-form-urlencoded'})
				r=self.s.post(self.base+path,data=data)
			else:
				self.s.headers.update({'Content-Type':'application/json'})
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
		res= self.callAPI('/dff/',1)
		self.user_data=json.loads(re.search('<script data-app-init-data type="application/json">(.*)</script>',res).group(1))
		if 'begin_battle_token' in res:
			self.begin_token=self.user_data['begin_battle_token']
		return res

	def jD(self,i):
		return json.dumps(i)
		
	def tutorial_proceed(self,step):
		data={}
		data['step']=int(step)
		return self.callAPI('/dff/tutorial/proceed',2,self.jD(data))

	def create_nickname(self,name):
		data={}
		data['nickname']=name
		return self.callAPI('/dff/tutorial/create_nickname',2,self.jD(data))

	def tutorial_battles(self):
		return self.callAPI('/dff/tutorial/battles',2,json.dumps({}))

	def login_bonus(self):
		return self.callAPI('/dff/login_bonus/receive',2,json.dumps({}))

	def tutorial_give_and_set_ability(self):
		return self.callAPI('/dff/tutorial/give_and_set_ability',2,json.dumps({}))

	def tutorial_begin_battle_session(self,step):
		data={}
		data['step']=int(step)
		return json.loads(self.callAPI('/dff/tutorial/begin_battle_session',2,self.jD(data)))['session_key']

	def genChkResult(self):
		self.crypter.setSeed()
		s=datetime.datetime.now().strftime("1%a %b %d %H:%M:%S %Y")
		s2=self.crypter.encrypt(s)
		s1=self.crypter.rsaEncryptText()
		return '%s_%s'%(s1,s2)
		
	def genBattle_win(self,input,force=False):
		data={}
		self.crypter.setSeed()
		if force:
			s2=self.crypter.encrypt(input)
			s1=self.crypter.rsaEncryptText()
			return '%s_%s'%(s1,s2)
		else:
			ChkResult=self.genChkResult()
			data['buddy']={}#TODO
			data['supporter']={}#TODO
			data['beast']={}#TODO
			data['score']={}#TODO
			data['log']={}#TODO
			data['initChkResult']=1
			data['initChkResultText']=ChkResult
			data['session_key']=self.user_session_key
			data['field']={}#TODO
			data['dynamicParam']={}
			data['cup']={}#TODO
			data1=self.crypter.rsaEncryptText()
			return '%s_%s'%(data1,Crypter().encrypt(json.dumps(data).replace(' ','')))

	def tutorial_battle_win(self,session_key):
		data={'results':self.genBattle_win('{"buddy":{"1":{"hp":6,"sa":[],"panel1":null,"panel2":1,"panel3":1,"ss_gauge":100}},"supporter":{"supporter_ss_gauge":0},"beast":{"synchronization_count":0,"remain_active_skill_num":0},"score":{"general":[{"no":1,"val1":5,"val2":0,"val3":0,"val4":0,"val5":0},{"no":2,"val1":139,"val2":6,"val3":0,"val4":0,"val5":0},{"no":3,"val1":0,"val2":0,"val3":0,"val4":0,"val5":0}],"specific":[{"no":1,"val1":1,"val2":0,"val3":0,"val4":0,"val5":0}]},"log":{"action_time":0,"action_num":0,"buddy_damage":0,"enemy_damage":0,"fps":0,"supporter_ss_use_num":0,"all_enemy_info":[],"enemy_info":[],"continue_infos":[],"buddy_ab_use_num":{},"buddy_ss_use_num":{},"enemy_ab_use_num":{},"max_combo_num":0},"initChkResult":1,"session_key":"%s"}'%(session_key),True)}
		self.s.headers.update({'Accept':'application/json, text/javascript, */*; q=0.01','X-Requested-With':'XMLHttpRequest','User-Session':'UNDEFINED_IN_API_JS','Accept-Encoding':'gzip, deflate','Accept-Language':'en-gb','Content-Type':'application/json','User-Agent':'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92'})
		return self.callAPI('/dff/tutorial/battle_win',2,self.jD(data))

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
		return self.callAPI('/dff/tutorial/update_recommend_party',2,self.jD(data))

	def tutorial_execute_gacha(self,step):
		data={}
		data['step']=int(step)
		return self.callAPI('/dff/tutorial/execute_gacha',2,self.jD(data))

	def tutorial_update_hero_equipment(self,step,equip_id):
		data={}
		data['step']=int(step)
		data['equipment_id']=int(equip_id)
		return self.callAPI('/dff/tutorial/update_hero_equipment',2,self.jD(data))

	def begin_session(self,battle_id):
		data={}
		data['battle_id']=battle_id
		data['begin_token']=self.begin_token
		return json.loads(self.callAPI('/dff/battle/begin_session',2,self.jD(data)))['session_key']

	def battle_init_data(self):
		return self.callAPI('/dff/battle/get_battle_init_data',1)
		
	def battle(self,battle_id):
		return self.callAPI('/dff/battle/?timestamp=%s&battle_id=%s'%(self.TS10(),battle_id),1)

	def battle_ts(self):
		return self.callAPI('/dff/battle/?timestamp=%s'%(self.TS10()),1)

	def battles(self):
		return self.callAPI('/dff/world/battles',1)
		
	def win(self):
		data={'results':self.genBattle_win('{"buddy":{"1":{"hp":170,"sa":[],"panel1":null,"panel2":4,"panel3":1,"ss_gauge":382},"2":{"hp":96,"sa":[],"panel1":null,"panel2":4,"ss_gauge":200},"3":{"hp":84,"sa":[],"panel1":null,"panel2":0,"panel3":2,"ss_gauge":215}},"supporter":{"supporter_ss_gauge":2},"beast":{"synchronization_count":0,"remain_active_skill_num":0},"score":{"general":[{"no":1,"val1":10,"val2":0,"val3":0,"val4":0,"val5":0},{"no":2,"val1":45,"val2":368,"val3":0,"val4":0,"val5":0},{"no":3,"val1":0,"val2":0,"val3":0,"val4":0,"val5":0}],"specific":[{"no":1,"val1":1,"val2":0,"val3":0,"val4":0,"val5":0}]},"log":{"action_num":10,"supporter_ss_use_num":0,"buddy_damage":1320,"enemy_damage":45,"continue_infos":[],"fps":29,"buddy_ab_use_num":{"1":{"panel1":3,"panel3":1},"2":{"panel1":3},"3":{"panel3":1,"panel2":2}},"buddy_ss_use_num":{},"enemy_ab_use_num":{},"max_combo_num":0,"action_time":78,"all_enemy_info":[[1,307004,1,1],[1,307007,1,1],[2,307004,1,1],[2,307004,1,1],[3,307001,1,1],[3,307007,1,1],[4,407001,1,1]],"enemy_info":[[4,407001,1,1,0]]},"initChkResult":1,"initChkResultText":"%s","session_key":"%s","field":{"elapsed_battle_time_from_beginning":24480},"dynamicParam":{},"cup":{"srqc":"|#cveez#;|#2#;|#iq#;281-#tt`hbvhf#;493-#tb#;\\^-#qbofm2#;ovmm-#qbofm3#;5-#qbofm4#;2~-#3#;|#iq#;:7-#tt`hbvhf#;311-#tb#;\\^-#qbofm2#;ovmm-#qbofm3#;5~-#4#;|#iq#;95-#tt`hbvhf#;326-#tb#;\\^-#qbofm2#;ovmm-#qbofm3#;1-#qbofm4#;3~~-#jojuDilSftvmu#;2-#tvqqpsufs`tt`hbvhf#;3-#cfbtu`tzodispoj{bujpo`dpvou#;1-#fmbqtfe`cbuumf`ujnf`gspn`cfhjoojoh#;35591~"}}'%(self.genChkResult(),self.battle_session_key),True)}
		return self.callAPI('/dff/battle/win',2,self.jD(data))
		
	def begin_battle(self,battle_id,session_key):
		data={}
		data['battle_id']=battle_id
		data['session_key']=session_key
		self.battle_session_key=session_key
		return self.callAPI('/dff/battle/begin_battle',2,self.jD(data))

	def doMission(self,id):
		self.init()
		self.battles()
		session_key=self.begin_session(id)
		self.begin_battle(id,session_key)
		self.battle(id)
		self.battle_init_data()
		self.win()
		
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
		session_key=self.tutorial_begin_battle_session(70)
		self.battle_ts()
		self.tutorial_battle_init_data()
		self.appspot.session_update()
		self.tutorial_battle_win(session_key)
		exit(1)
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
	#a.setUser('26bbb48d-63f4-404d-a7bb-0bf2264ac569','','QiEJjdiAWAtGsEtrnIEhAOXOI8LqfD')
	a.login()
	#a.doMission(307001)
	a.completeTutorial()