from crypt import Crypter
import rsa

#with open('public.pem', mode='rb') as pp:
#	keydata = pp.read()
#publickey = rsa.PublicKey.load_pkcs1_openssl_pem(keydata)
#print rsa.encrypt('ss', publickey)
#exit(1)

c=Crypter()
c.setSeed('6E 7E 4C 7D 4E 3F 7A 35 3B 21 2B 2E 5F 57 61 45')
plain='1Sun Nov 19 00:15:25 2017'
tmp='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'
#plain='{"buddy":{"1":{"hp":6,"sa":[],"panel1":null,"panel2":1,"panel3":1,"ss_gauge":100}},"supporter":{"supporter_ss_gauge":0},"beast":{"synchronization_count":0,"remain_active_skill_num":0},"score":{"general":[{"no":1,"val1":5,"val2":0,"val3":0,"val4":0,"val5":0},{"no":2,"val1":139,"val2":6,"val3":0,"val4":0,"val5":0},{"no":3,"val1":0,"val2":0,"val3":0,"val4":0,"val5":0}],"specific":[{"no":1,"val1":1,"val2":0,"val3":0,"val4":0,"val5":0}]},"log":{"action_time":0,"action_num":0,"buddy_damage":0,"enemy_damage":0,"fps":0,"supporter_ss_use_num":0,"all_enemy_info":[],"enemy_info":[],"continue_infos":[],"buddy_ab_use_num":{},"buddy_ss_use_num":{},"enemy_ab_use_num":{},"max_combo_num":0},"initChkResult":1,"session_key":"77814e41a24e4afcf83c31a62904c4f0"}'
#rsa,aes=tmp.split('_')
#print len(tmp),len(aes)


#crp= c.encrypt(plain)
#print '"%s"'%crp
print '"%s"'%c.decrypt(tmp)
res= c.rsaEncryptText()
if 'Pf3y009NkU8NV5gskWAEVkzpR' in res:
	print res
	exit(1)